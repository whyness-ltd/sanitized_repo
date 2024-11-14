#----------------------------------------------------------------------
# Whyness Queue runner processing
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

import datetime
import logging
import pytz
import time

from datetime import datetime

from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from whyness_django.models import STATUS_INACTIVE
from whyness_django.models import STATUS_ACTIVE
from whyness_django.models import TRANSCRIPT_STATUS_INACTIVE
from whyness_django.models import TRANSCRIPT_STATUS_ACTIVE
from whyness_django.models import TRANSCRIPT_STATUS_SENT_FOR_TRANSCRIPTION
from whyness_django.models import TRANSCRIPT_STATUS_IN_PROGRESS
from whyness_django.models import TRANSCRIPT_STATUS_TRANSCRIBED
from whyness_django.models import TRANSCRIPT_STATUS_TRANSCRIBE_FAILED
from whyness_django.models import TRANSCRIPT_STATUS_REPRESENTATIONAL_SYSTEM
from whyness_django.models import TRANSCRIPT_STATUS_NEEDS_CONVERTING
from whyness_django.models import TRANSCRIPT_STATUS_DELETED
from whyness_django.models import TRANSCRIPT_STATUS_ERROR
from whyness_django.models import Audio

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Queue runner'

    def add_arguments(self, parser):
        parser.add_argument(
            '--status',
            action='store_true',
            help="Status",
        )
        parser.add_argument(
            '--start',
            action='store_true',
            help="Start the queue to process transcriptions",
        )

    def handle(self, *args, **options):
        SLEEP_SECONDS = 60
        msg = "Config: {}".format(settings.BUILD_CONFIG)
        self.stdout.write(msg)
        if options['status']:
            datas = Audio.objects.filter(Q(
                status=TRANSCRIPT_STATUS_INACTIVE) | Q(
                status=TRANSCRIPT_STATUS_SENT_FOR_TRANSCRIPTION) | Q(
                status=TRANSCRIPT_STATUS_IN_PROGRESS) | Q(
                status=TRANSCRIPT_STATUS_TRANSCRIBED) | Q(
                status=TRANSCRIPT_STATUS_NEEDS_CONVERTING))
            msg = "Stories to update: {}".format(len(datas))
            self.stdout.write(msg)
            for data in datas:
                msg = "Story: {}:{}".format(data.create_date, data)
                self.stdout.write(msg)
        if options['start']:
            while True:
                datas = Audio.objects.filter(Q(
                    status=TRANSCRIPT_STATUS_INACTIVE) | Q(
                    status=TRANSCRIPT_STATUS_SENT_FOR_TRANSCRIPTION) | Q(
                    status=TRANSCRIPT_STATUS_IN_PROGRESS) | Q(
                    status=TRANSCRIPT_STATUS_TRANSCRIBED) | Q(
                    status=TRANSCRIPT_STATUS_NEEDS_CONVERTING))
                msg = "Stories to update: {} - {}".format(
                    len(datas), datetime.now()
                )
                self.stdout.write(msg)
                for data in datas:
                    msg = "Story: {}:{}".format(
                        data.id,
                        data.status,
                        data.create_date,
                    )
                    self.stdout.write(msg)
                    if data.status == TRANSCRIPT_STATUS_ACTIVE:
                        msg = '{}: Transcribe'.format(data.status)
                        self.stdout.write(msg)
                        data.transcribe()
                    if data.status == TRANSCRIPT_STATUS_SENT_FOR_TRANSCRIPTION:
                        msg = '{}: Transcribe sent'.format(data.status)
                        self.stdout.write(msg)
                        data.transcribe_status_check()
                    if data.status == TRANSCRIPT_STATUS_NEEDS_CONVERTING:
                        msg = '{}: Transcribe convert'.format(data.status)
                        self.stdout.write(msg)
                        data.convert_for_transcription()
                    if data.status == TRANSCRIPT_STATUS_TRANSCRIBED:
                        msg = '{}: Represent'.format(data.status)
                        self.stdout.write(msg)
                        data.get_representational_system()
                    if data.status == TRANSCRIPT_STATUS_REPRESENTATIONAL_SYSTEM:
                        msg = '{}: MBTI'.format(data.status)
                        self.stdout.write(msg)
                        data.process_mbti()
                tz_gmt = pytz.timezone('Europe/London')
                now = datetime.now(tz=tz_gmt)
                msg = "Sleeping for {}s: {}".format(SLEEP_SECONDS, now)
                logger.info(msg)
                time.sleep(SLEEP_SECONDS)
