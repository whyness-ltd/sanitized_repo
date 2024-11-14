#----------------------------------------------------------------------
# Whyness models
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

import boto3
import json
import logging
import os
import subprocess
import time
import uuid
from botocore.exceptions import ClientError
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import urllib.request
from whyness_django.rule_based_preferred_representational_system_whyness import rule_based_rs
from whyness_ml_models.MBTI_Prediction import MBTIPrediction
from whyness_ml_models.models import MBTI

logger = logging.getLogger(__name__)

STATUS_INACTIVE = 0
STATUS_ACTIVE = 1
STATUS_DELETED = 8

STATUS_CHOICES = (
    (STATUS_INACTIVE, ('Inactive')),
    (STATUS_ACTIVE, ('Active')),
)

TRANSCRIPT_STATUS_INACTIVE = 0
TRANSCRIPT_STATUS_ACTIVE = 1
TRANSCRIPT_STATUS_SENT_FOR_TRANSCRIPTION = 2
TRANSCRIPT_STATUS_IN_PROGRESS = 3
TRANSCRIPT_STATUS_TRANSCRIBED = 4
TRANSCRIPT_STATUS_TRANSCRIBE_FAILED = 5
TRANSCRIPT_STATUS_REPRESENTATIONAL_SYSTEM = 6
TRANSCRIPT_STATUS_NEEDS_CONVERTING = 7
TRANSCRIPT_STATUS_MBTI = 8
TRANSCRIPT_STATUS_DELETED = 98
TRANSCRIPT_STATUS_ERROR = 99

TRANSCRIPT_STATUS_CHOICES = (
    (TRANSCRIPT_STATUS_INACTIVE, ('Inactive')),
    (TRANSCRIPT_STATUS_ACTIVE, ('Active')),
    (TRANSCRIPT_STATUS_SENT_FOR_TRANSCRIPTION, ('Sent for transcription')),
    (TRANSCRIPT_STATUS_IN_PROGRESS, ('Transcription in progress')),
    (TRANSCRIPT_STATUS_TRANSCRIBED, ('Transcribed')),
    (TRANSCRIPT_STATUS_TRANSCRIBE_FAILED, ('Transcription failed')),
    (TRANSCRIPT_STATUS_REPRESENTATIONAL_SYSTEM, ('Representational system')),
    (TRANSCRIPT_STATUS_MBTI, ('MBTI')),
    (TRANSCRIPT_STATUS_DELETED, ('Deleted')),
)

UUID_NULL = uuid.UUID('00000000-0000-0000-0000-000000000000')

class AuthUser(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=250)
    name = models.CharField(max_length=250, default='')
    email = models.CharField(max_length=250, default='')
    status = models.SmallIntegerField(default=STATUS_ACTIVE)
    xref = models.UUIDField('AuthUser Reference', default=uuid.uuid4)
    update_ip = models.GenericIPAddressField(default='::1')
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}: {}".format(self.id, self.uid)
        return ret

    def save(self, *args, **kwargs):
        if not self.xref:
            self.xref = uuid.uuid4()
        super(AuthUser, self).save(*args, **kwargs)

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=500)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)
    sort_order = models.IntegerField()
    update_ip = models.GenericIPAddressField(default='::1')
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        ret = "{}: {}".format(self.sort_order, self.question)
        return ret

    def save(self, *args, **kwargs):
        if not self.sort_order:
            max_sort_order = Question.objects.order_by('-sort_order')[1].get()
            msg = "max_sort_order: {}".format(max_sort_order)
            logger.debug()
            self.sort_order = max_sort_order + 1
        super(Question, self).save(*args, **kwargs)

    class Meta:
        ordering = ['sort_order']

def file_field_callable(instance, filename):
    file_root, file_ext = os.path.splitext(filename)
    msg = 'File root: {}'.format(file_root)
    logger.debug(msg)
    file_root = str(uuid.uuid4())
    msg = 'File root: {}'.format(file_root)
    logger.debug(msg)
    msg = 'File ext: {}'.format(file_ext)
    logger.debug(msg)
    if settings.BUILD_CONFIG == settings.BUILD_PROD:
        upload_to = "media"
    else:
        upload_to = "media_dev"
    ret = '{}/{}{}'.format(upload_to, file_root, file_ext)
    return ret

class Audio(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField('title', default='', max_length=75)
    media = models.FileField(upload_to=file_field_callable)
    transcript = models.TextField(default="")
    transcript_s3 = models.TextField(default="")
    transcript_json = models.TextField(default="")
    transcribe_job_name = models.CharField(default="", max_length=100)
    transcribe_status = models.CharField(default="", max_length=20)
    #Valid Values: QUEUED | IN_PROGRESS | FAILED | COMPLETED
    transcribe_status_json = models.TextField(default="")
    representational_system = models.TextField(default="")
    status = models.SmallIntegerField(
        choices=TRANSCRIPT_STATUS_CHOICES,
        default=TRANSCRIPT_STATUS_ACTIVE
    )
    update_ip = models.GenericIPAddressField(default='::1')
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = ''
        super(Audio, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.media.delete()
        self.status = TRANSCRIPT_STATUS_DELETED
        super(Audio, self).delete(*args, **kwargs)

    def convert_for_transcription(self):
        """Convert an unsupported audio file
        into one that can be transcribed"""
        s3 = boto3.client('s3',
            region_name=settings.AWS_REGION_NAME,
        )
        basename = os.path.basename(self.media.name)
        file_root, file_ext = os.path.splitext(basename)
        local_file_unsupported = '{}/{}{}'.format(settings.TMP_DIR, file_root, file_ext)
        local_file_supported = '{}/{}{}'.format(settings.TMP_DIR, file_root, '.webm')
        try:
            msg = "Downloading: {}".format(local_file_unsupported)
            logger.debug(msg)
            s3.download_file(
                settings.AWS_STORAGE_BUCKET_NAME,
                self.media.name,
                local_file_unsupported
            )
        except ClientError as error:
            logger.error(error)
            self.status = TRANSCRIPT_STATUS_ERROR
            self.save()
            return False

        # Create a supported file name and convert
        try:
            msg = "Converting to: {}".format(local_file_supported)
            logger.debug(msg)
            subprocess.run([
                settings.FFMPEG,
                '-i', local_file_unsupported,
                local_file_supported
            ])
        except subprocess.CalledProcessError as error:
            logger.error(error)
            self.status = TRANSCRIPT_STATUS_ERROR
            self.save()
            return False

        try:
            #s3_client.upload_file(file_name, bucket, object_name)
            msg = "Uploading: {}".format(local_file_supported)
            logger.debug(msg)
            new_media = 'media/{}{}'.format(file_root, '.webm')
            self.media.name = new_media
            response = s3.upload_file(
                local_file_supported,
                settings.AWS_STORAGE_BUCKET_NAME,
                self.media.name,
            )
            self.save()
        except ClientError as error:
            logger.error(error)
            return False
        transcribe = boto3.client(
            'transcribe',
            region_name=settings.AWS_REGION_NAME,
        )
        if self.transcribe_job_name:
            # Delete the old transcription job
            try:
                msg = "Deleting old transcription job: {}".format(self.transcribe_job_name)
                logger.debug(msg)
                transcribe.delete_transcription_job(
                    TranscriptionJobName=self.transcribe_job_name,
                )
            except ClientError as error:
                logger.error(error)
        else:
            # Create a transcription job name
            self.transcribe_job_name = str(uuid.uuid4())
        # Submit new transcription job
        msg = "Starting new transcription job: {}".format(self.transcribe_job_name)
        logger.debug(msg)
        self.transcribe_status_json = transcribe.start_transcription_job(
            TranscriptionJobName=self.transcribe_job_name,
            Media={'MediaFileUri': self.media.url},
            LanguageCode='en-GB'
        )
        msg = "Transcribe request sent after conversion"
        logger.debug(msg)
        self.status = TRANSCRIPT_STATUS_SENT_FOR_TRANSCRIPTION
        super(Audio, self).save()
        # Tidy up and delete local files
        try:
            os.remove(local_file_unsupported)
            os.remove(local_file_supported)
        except:
            msg = "Unable to delete {} {}".format(local_file_unsupported, local_file_supported)
            logger.warning(msg)

    def transcribe(self):
        """Start a transcription"""
        transcribe = boto3.client(
            'transcribe',
            region_name=settings.AWS_REGION_NAME,
        )
        if not self.transcribe_job_name:
            self.transcribe_job_name = str(uuid.uuid4())
        msg = 'Media to transcribe: {}'.format(self.media.url)
        logger.debug(msg)

        file_root, file_ext = os.path.splitext(self.media.url)
        if file_ext == '.aac':
            self.status = TRANSCRIPT_STATUS_NEEDS_CONVERTING
        else:
            transcribe.start_transcription_job(
                TranscriptionJobName=self.transcribe_job_name,
                Media={'MediaFileUri': self.media.url},
                LanguageCode='en-GB'
            )
            msg = "Transcribe request sent".format()
            logger.debug(msg)
            self.status = TRANSCRIPT_STATUS_SENT_FOR_TRANSCRIPTION
        super(Audio, self).save()

    def transcribe_status_check(self):
            if not self.transcribe_job_name:
                msg = 'Audio {} does not have a job name!'.format(audio.id)
                logger.error(msg)
            else:
                transcribe = boto3.client(
                    'transcribe',
                    region_name=settings.AWS_REGION_NAME,
                )
                self.transcribe_status_json = transcribe.get_transcription_job(
                    TranscriptionJobName=self.transcribe_job_name)
                self.transcribe_status = self.transcribe_status_json['TranscriptionJob']['TranscriptionJobStatus']
                msg = self.transcribe_status_json
                logger.debug(msg)
                msg = self.transcribe_status
                logger.debug(msg)
                super(Audio, self).save()
                if self.transcribe_status == 'COMPLETED':
                    self.transcribe_get_transcription()
                if self.transcribe_status == 'FAILED':
                    self.status = TRANSCRIPT_STATUS_ERROR
                    super(Audio, self).save()

    def transcribe_get_transcription(self):
        if not self.transcribe_job_name:
            msg = 'Audio {} does not have a job name!'.format(audio.id)
            logger.error(msg)
        else:
            self.transcript_s3 = self.transcribe_status_json['TranscriptionJob']['Transcript']['TranscriptFileUri']
            super(Audio, self).save()

            with urllib.request.urlopen(self.transcript_s3) as f:
                self.transcript_json = f.read().decode('utf-8')
                msg = "transcribe_get_transcription status: {}".format(f.status)
                logger.debug(msg)
            super(Audio, self).save()

            transcript_json = json.loads(self.transcript_json)
            self.transcript = transcript_json['results']['transcripts'][0]['transcript']
            self.status = TRANSCRIPT_STATUS_TRANSCRIBED
            super(Audio, self).save()

    def get_representational_system(self):
        if self.status == TRANSCRIPT_STATUS_TRANSCRIBED:
            out = rule_based_rs(self.transcript)
            logger.debug(out)
            self.representational_system = out
            self.status = TRANSCRIPT_STATUS_REPRESENTATIONAL_SYSTEM
            super(Audio, self).save()

    def process_mbti(self):
        if self.status == TRANSCRIPT_STATUS_REPRESENTATIONAL_SYSTEM:
            # Collect all transcriptions
            stories = ""
            msg = "Getting audios"
            logger.debug(msg)
            audios = Audio.objects.filter(
                user=self.user,
                status__lte=TRANSCRIPT_STATUS_DELETED,
            )
            for audio in audios:
                stories = "{} {}".format(stories, audio.transcript)
            msg = "Stories is: {}".format(stories)
            logger.debug(msg)

            #Feed them into the MBTI function
            prediction = MBTIPrediction()
            mbti_ie, mbti_ns, mbti_tf, mbti_pj  = prediction.predict_MBTI(stories)

            #Add the output to an MBTI record
            data = MBTI()
            data.user = self.user
            data.IE = mbti_ie
            data.NS = mbti_ns
            data.TF = mbti_tf
            data.PJ = mbti_pj
            data.update_ip = self.update_ip
            ret = data.save()
            logger.debug(ret)

            self.status = TRANSCRIPT_STATUS_MBTI
            super(Audio, self).save()

    def __str__(self):
        if self.media.name:
            msg = '{}:{}:{}'.format(self.id, self.title, self.media.name)
            return msg
        else:
            msg = '{}:{}'.format(self.id, self.title)
            return msg
    class Meta:
        verbose_name_plural = 'Audio'
        ordering = ['-id']

class UserAgent(models.Model):
    id = models.AutoField(primary_key=True)
    useragent = models.CharField(blank=True, max_length=500, unique=True)

    def __str__(self):
        ret = "{}: {}".format(self.id, self.useragent)
        return ret

class ErrorLog(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    hostip = models.GenericIPAddressField(null=True)
    hostname = models.CharField(blank=True, max_length=500)
    useragent = models.CharField(blank=True, max_length=500)
    errorcode = models.TextField('Error code', blank=True)
    errormessage = models.TextField('Error message', blank=True)

    def __str__(self):
        ret = '{}: {}:{}'.format(self.date, self.errorcode, self.errormessage)
        return ret

class TypeAttributes(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(default="")

    def __str__(self):
        ret = "{}: {}".format(self.id, self.title)
        return ret

    class Meta:
        verbose_name_plural = 'Type attributes'

class TrackerItem(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        ret = "{}".format(self.title)
        return ret

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = self.title
        super(TrackerItem, self).save(*args, **kwargs)

class TrackerLog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    item = models.ForeignKey(TrackerItem, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(default='::1')
    useragent = models.ForeignKey(UserAgent, on_delete=models.PROTECT)
    method = models.CharField(default="", max_length=20)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}:{}:{}".format(self.create_date, self.user, self.item)
        return ret

    class Meta:
        ordering = ['-id']

class Profession(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        ret = "{}".format(self.title)
        return ret

    class Meta:
        ordering = ['title']

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    attributes = models.ManyToManyField(TypeAttributes)

    def __str__(self):
        ret = "{}: {}".format(self.id, self.title)
        return ret

    class Meta:
        ordering = ['title']
