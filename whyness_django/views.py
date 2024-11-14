#----------------------------------------------------------------------
# Whyness views
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

"""
"""

import base64
import boto3
import io
import json
import logging
import firebase_admin
import os
import tempfile
import urllib

from firebase_admin import credentials
from firebase_admin import auth

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404

from oauth2_provider.views.generic import ProtectedResourceView

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from whyness_django.models import AuthUser
from whyness_django.models import Audio, Question
from whyness_django.models import Profession, Role, TypeAttributes
from whyness_django.models import TrackerLog, TrackerItem, UserAgent

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

from whyness_django.serializers import AudioSerializer, AudioResponseSerializer
from whyness_django.serializers import QuestionSerializer
from whyness_django.serializers import UserProfileSerializer
from whyness_django.serializers import ProfessionSerializer
from whyness_django.serializers import RoleSerializer
from whyness_django.serializers import TypeAttributesSerializer
from whyness_django.serializers import AuthUserSerializer
from whyness_django.serializers import UserPWResetSerializer
from whyness_django.serializers import UserStatusSerializer
from whyness_django.serializers import VersionSerializer

from whyness_appgyver_polls.models import DreamJob
from whyness_appgyver_polls.models import SweetSpot

from whyness_mixpanel.models import Event

logger = logging.getLogger(__name__)

#Initialise firebase creds from S3 bucket
AWS_REGION_NAME = 'eu-west-1'
if 'AWS_REGION_NAME' in os.environ:
    AWS_REGION_NAME = os.environ['AWS_REGION_NAME']
s3 = boto3.resource('s3', region_name=AWS_REGION_NAME)
bucket = s3.Bucket('whyness-private-keys')
object = bucket.Object('firebase/whyness-b2f3f-firebase-adminsdk-sslpz-f37a1835f3.json')
tmp = tempfile.NamedTemporaryFile()

with open(tmp.name, 'wb') as f:
    try:
        object.download_fileobj(f)
        f.seek(0)
        cred = credentials.Certificate(tmp.name)
        firebase_app = firebase_admin.initialize_app(cred)
    except BaseException as err:
        msg = "Firebase credentials not found or not accessible: {}".format(err)
        logger.debug(msg)

def get_auth_user(request=None):
    """Returns idToken"""
    # TODO Urgent
    # As soon as the app is configured to always deliver valid tokens
    # this function should use google.auth.jwt/google.oauth2 or similar
    user = None
    uid = None

    # get Authorizattion Bearer token
    msg = '{}'.format(request.headers)
    logger.debug(msg)
    if 'Authorization' in request.headers:
        auth_header = request.headers.get('Authorization')
        msg = "Authorization: {}".format(auth_header)
        logger.debug(msg)
    else:
        msg = "No authorization header"
        logger.debug(msg)
        auth_header = None

    if auth_header:
        try:
            (token_header, token_payload, token_signature) = auth_header.split(".")
            token_remainder = len(token_payload) % 4
            if token_remainder == 3:
                token_payload = token_payload + '='
            elif token_remainder == 2:
                token_payload = token_payload + '=='
            elif token_remainder == 1:
                token_payload = token_payload + '==='
            strj = base64.b64decode(token_payload)
            msg = 'jwt-payload: {}'.format(strj)
            logger.debug(msg)
            payload_json = json.loads(strj)
            logger.debug(msg)
        except Exception as e:
            msg = "Could not split token from: {}: {}".format(auth_header, e)
            logger.debug(msg)

        try:
            #decoded_token = auth.verify_id_token(id_token)
            uid = payload_json['user_id']
            #msg = 'Decoded token: {}'.format(decoded_token)
            #logger.debug(msg)
        except Exception as e:
            msg = "Could not verify token: {}".format(e)
            logger.debug(msg)

    if uid:
        try:
            user = AuthUser.objects.get(uid=uid)
            msg = "User: {}".format(user)
            logger.debug(msg)
        except:
            # Create the user if they don'e exist
            user = AuthUser(uid=uid)
            user.save()
        try:
            if 'email' in payload_json:
                msg = "Email: {}".format(payload_json['email'])
                logger.debug(msg)
                user.email = payload_json['email']
            if 'name' in payload_json:
                msg = "Name: {}".format(payload_json['name'])
                logger.debug(msg)
                user.name = payload_json['name']
            user.save()
        except Exception as e:
            msg = e
            logger.debug(msg)

    return user

def home(request):

    flatpage = FlatPage.objects.get(url="/home/")
    context = {
        "flatpage": flatpage,
    }
    return render(request, 'flatpages/default.html', context)

def get_host_info(request=None):
    """Returns address, host and agent for a request"""
    remote_addr = ''
    remote_host = ''
    if request:
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            remote_addr = request.META['HTTP_X_FORWARDED_FOR']
        elif 'REMOTE_ADDR' in request.META:
            remote_addr = request.META['REMOTE_ADDR']
        if remote_addr.count(',') > 0:
            # If this address is behind a proxy, then only use the first
            remote_addr = remote_addr.split(',')[0]
        if 'REMOTE_HOST' in request.META:
            remote_host = request.META['REMOTE_HOST']

    return (remote_addr, remote_host)

def get_useragent(request=None):
    """Get user agent from request, adding any not found
    An attempt at recording an agent before api double requests and tries to insert duplicate
    """
    msg = 'get_useragent'
    logger.debug(msg)
    if not request:
        return None
    ret = None
    user_agent = None
    if 'HTTP_USER_AGENT' in request.META:
        user_agent = request.META['HTTP_USER_AGENT']
    if user_agent:
        msg = 'User agent presented: {}'.format(user_agent)
        logger.debug(msg)
        try:
            ret = UserAgent.objects.get(useragent=user_agent)
        except UserAgent.DoesNotExist:
            ret = UserAgent(useragent=user_agent)
            ret.save()
    else:
        try:
            ret = UserAgent.objects.get(useragent=USER_AGENT_NONE)
        except UserAgent.DoesNotExist:
            msg = 'Unable to find (none)'
            logger.debug(msg)
            ret = UserAgent(useragent=USER_AGENT_NONE)
            ret.save()
    return ret

def tracker_log(
        activity=None,
        request=None,
        user=None,
        activityresult=None):

    msg = 'log_activity: {}:{}'.format(activity, request.method)
    logger.debug(msg)
    if not activity:
        return None
    if not request:
        return None
    useragent = get_useragent(request)
    try:
        activity = TrackerItem.objects.get(title=activity)
    except TrackerItem.DoesNotExist:
        activity = TrackerItem(title=activity)
        activity.save()

    (remote_addr, remote_host) = get_host_info(request)

    activity_log = TrackerLog(item=activity)
    activity_log.ip = remote_addr
    activity_log.activityresult = activityresult
    if user:
        activity_log.user = user
    else:
        user = AuthUser.objects.get(pk=1)
        activity_log.user = user

    if useragent:
        activity_log.useragent = useragent
    if request.method:
        activity_log.method = request.method
    try:
        activity_log.save()
        mpe = Event()
        mpe.event = activity_log.item.title
        mpe.insert_id = activity_log.id
        mpe.time = int(activity_log.create_date.timestamp())
        mpe.user = str(user.id)
        mpe.ip = activity_log.ip
        mpe.useragent = activity_log.useragent.useragent
        mpe.method = activity_log.method
        mpe.send()
    except Exception as err:
        msg = 'Error saving Tracker {}'.format(err)
        logger.error(msg)

    return None

def media_list(request):

    try:
        media = Audio.objects.all()
    except Exception as err:
        msg = 'Error finding Audio: {}'.format(err)
        logger.error(msg)
    context = {
        "media": media,
        "settings": settings,
    }
    return render(request, 'whyness_django/media_list.html', context)

def media_item(request, id):

    try:
        media = Audio.objects.get(pk=id)
    except ObjectDoesNotExist as err:
        # No Audio with that id
        msg = 'Audio not found for: {}: {}'.format(id, err)
        logger.debug(msg)
    except Exception as err:
        msg = 'Error finding Audio: {}: {}'.format(id, err)
        logger.error(msg)
    context = {
        "media": media,
        "settings": settings,
    }
    return render(request, 'whyness_django/media_item.html', context)

class ApiMedia(APIView):
    """
    Manage Media
    """
    permission_classes = [AllowAny]

    def get(self, request, id=None, format=None):
        """
        Return media
        """
        user = get_auth_user(request)
        if user:
            msg = "UserID: {}".format(user.id)
            logger.debug(msg)
        else:
            raise Http404

        tracker_log(
            activity='media',
            request=request,
            user=user,
        )

        if id:
            msg = "Media: {}".format(id)
        else:
            msg = "Media listing"
        logger.debug(msg)
        try:
            if id:
                audio = Audio.objects.get(user=user, pk=id)
            else:
                audio = Audio.objects.filter(user=user).order_by('-create_date')
                if not len(audio):
                    audio = [Audio(),]
        except Audio.DoesNotExist:
            raise Http404

        #TRANSCRIPT_STATUS_INACTIVE
        #TRANSCRIPT_STATUS_IN_PROGRESS
        #TRANSCRIPT_STATUS_TRANSCRIBED
        #TRANSCRIPT_STATUS_TRANSCRIBE_FAILED
        #TRANSCRIPT_STATUS_DELETED
        if id and audio.status == TRANSCRIPT_STATUS_ACTIVE:
            audio.transcribe()
        if id and audio.status == TRANSCRIPT_STATUS_SENT_FOR_TRANSCRIPTION:
            audio.transcribe_status_check()
        if id and audio.status == TRANSCRIPT_STATUS_NEEDS_CONVERTING:
            audio.convert_for_transcription()
        if id and audio.status == TRANSCRIPT_STATUS_TRANSCRIBED:
            audio.get_representational_system()
        if id:
            return Response(AudioResponseSerializer(audio).data)
        else:
            return Response(AudioResponseSerializer(audio, many=True).data)

    def put(self, request, format=None):
        """
        Store media
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='media',
            request=request,
            user=user,
        )

        (remote_addr, remote_host) = get_host_info(request)

        msg = "Put media: {}".format(
            request.data,
        )
        logger.debug(msg)

        try:
            media_response = AudioSerializer(data=request.data)
            if 'media' in request.FILES:
                msg = "Setting title: {}".format(request.FILES['media'])
                logger.debug(msg)
                media_response.title = request.FILES['media']
            if 'question' not in request.query_params:
                question = Question.objects.get(pk=9)
                media_response.question = question
                msg = "Question set to: {}".format(question.id)
                logger.debug(msg)
        except Exception as err:
            msg = "An Error occured processing this media: {}".format(err)
            logger.warning(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        if media_response.is_valid():
            (remote_addr, remote_host) = get_host_info(request)
            result = media_response.save(user=user, update_ip=remote_addr)
        else:
            return Response(media_response.errors, status=status.HTTP_400_BAD_REQUEST)
        result.transcribe()
        # Use AudioResponseSerializer to avoid sending media
        return Response(AudioResponseSerializer(result).data)

    def delete(self, request, id=None, format=None):
        """
        Delete media
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='media',
            request=request,
            user=user,
        )

        errors = {}
        (remote_addr, remote_host) = get_host_info(request)
        msg = "Delete media: {}".format(id)
        logger.debug(msg)
        if not id:
            errors = '{"media": ["A media id is required"]}'
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            audio = Audio.objects.get(user=user, pk=id)
            audio.delete
            msg = "__name__:Media.delete: {}: {}: {}".format(id, audio.title, 'Media deleted')
            logger.debug(msg)
        except Audio.DoesNotExist:
            msg = "__name__:Media.delete: {}: {}: {}".format(id, '404', 'Media does not exist')
            logger.error(msg)
            raise Http404

        return Response(status=status.HTTP_204_NO_CONTENT)

class ApiQuestion(APIView):
    """
    Available Questions
    """
    permission_classes = [AllowAny]

    def get(self, request, id=None, format=None):
        """
        Return Question
        """
        user = get_auth_user(request)
        if user:
            msg = "UserID: {}".format(user.id)
            logger.debug(msg)
        else:
            pass
            #raise Http404
        if id:
            msg = "Question: {}".format(id)
        else:
            msg = "Question listing"
        logger.debug(msg)
        try:
            if id:
                question = Question.objects.get(pk=id)
            else:
                question = Question.objects.all().order_by('sort_order')
        except Audio.DoesNotExist:
            raise Http404

        if id:
            return Response(QuestionSerializer(question).data)
        else:
            return Response(QuestionSerializer(question, many=True).data)

class ApiUser(APIView):
    """User name"""
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Return a user's name
        """
        user = get_auth_user(request)
        if user:
            msg = "UserID: {}".format(user.id)
            logger.debug(msg)
        else:
            raise Http404

        tracker_log(
            activity='user_name',
            request=request,
            user=user,
        )

        return Response(AuthUserSerializer(user).data)

    def put(self, request, format=None):
        """
        Update a user's name
        """
        user = get_auth_user(request)
        if user:
            msg = "UserID: {}".format(user.id)
            logger.debug(msg)
        else:
            raise Http404

        tracker_log(
            activity='user_name',
            request=request,
            user=user,
        )

        try:
            user_response = AuthUserSerializer(instance=user, data=request.data)
        except Exception as err:
            msg = "An Error occured serializing user: {}".format(err)
            logger.warning(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        if user_response.is_valid():
            (remote_addr, remote_host) = get_host_info(request)
            result = user_response.save(user=user, update_ip=remote_addr)
        else:
            msg = "An Error occured saving user: {}".format(err)
            logger.warning(msg)
            return Response(user_response.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(AuthUserSerializer(result).data)

class ApiUserProfile(APIView):
    """
    User profile
    """
    permission_classes = [AllowAny]

    def get(self, request, id=None, format=None):
        """
        Return Question
        """
        user = get_auth_user(request)
        if user:
            msg = "UserID: {}".format(user.id)
            logger.debug(msg)
        else:
            pass
            #raise Http404

        tracker_log(
            activity='user_profile',
            request=request,
            user=user,
        )

        visual = 0
        auditory = 0
        kinesthetic = 0
        auditory_digital = 0

        audios = Audio.objects.filter(user=user)
        for audio in audios:
            if audio.representational_system and user:
                #logger.debug(audio.representational_system)
                data = json.loads(audio.representational_system)
                #logger.debug(data)
                visual+= int(data["visual"])
                auditory+= int(data["auditory"])
                kinesthetic+= int(data["kinesthetic"])
                auditory_digital+= int(data["auditory_digital"])
        profile = {
            "representational_system": {
                "visual": visual,
                "auditory": auditory,
                "kinesthetic": kinesthetic,
                "auditory_digital": auditory_digital
            }
        }

        return Response(UserProfileSerializer(profile).data)

class ApiUserPWReset(APIView):
    """
    Send password reset to Firebase
    """
    permission_classes = []
    authentication_classes = []

    def post(self, request, format=None):
        """
        Return Confirmation the password reset has been requested
        """
        email=None
        tracker_log(
            activity='user_pw_reset',
            request=request,
            user=None,
        )
        # Get the firebase api key
        ssm = boto3.client('ssm', region_name='eu-west-1')
        try:
            Parameter = ssm.get_parameter(Name='FIREBASE_API_KEY = "REMOVED"
            api_key = Parameter['Parameter']['Value']
        except BaseException as err:
            print(f"Unexpected error getting parameter: {err=}, {type(err)=}")
            return None

        try:
            user_response = UserPWResetSerializer(data=request.data)
        except Exception as err:
            msg = "An Error occured serializing PWReset: {}".format(err)
            logger.warning(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        data = {}
        if user_response.is_valid():
            # Call the url
            url_google = "https://REMOVED
            url = "{}:{}?key={}".format(url_google, 'sendOobCode', api_key)
            data = {
                'requestType':'PASSWORD_RESET',
                'email': user_response.validated_data['email']
            }
            logger.debug(url)
            data = json.dumps(data).encode('utf-8')
            logger.debug(data)
            # Send data to url
            headers = {'Content-Type': 'application/json'}
            req = urllib.request.Request(url, headers=headers, method='POST')
            url_ret = urllib.request.urlopen(req, data=data)
            data = url_ret.read().decode('utf-8')
            data = json.loads(data)
        else:
            msg = "PWReset user response is invalid"
            logger.warning(msg)
            return Response(user_response.errors, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(data)

        return Response(UserPWResetSerializer(data).data)

class ApiUserStatus(APIView):
    """
    User status
    - sweetspotcompleted
    - dreamjobcompleted
    """
    permission_classes = [AllowAny]

    def get(self, request, id=None, format=None):
        """
        Return Question
        """
        user = get_auth_user(request)
        if user:
            msg = "UserID: {}".format(user.id)
            logger.debug(msg)
        else:
            raise Http404

        tracker_log(
            activity='user_status',
            request=request,
            user=user,
        )

        sweetspot = SweetSpot.objects.filter(user=user).count()
        logger.debug(sweetspot)
        if sweetspot:
            sweetspot_completed = True
        else:
            sweetspot_completed = False
        dreamjob = DreamJob.objects.filter(user=user).count()
        logger.debug(dreamjob)
        if dreamjob:
            dreamjob_completed = True
        else:
            dreamjob_completed = False

        stories = ""
        audios = Audio.objects.filter(
            user=user,
            status__lte=TRANSCRIPT_STATUS_DELETED,
        )
        for audio in audios:
            stories = "{} {}".format(stories, audio.transcript)
        word_list = stories.split()
        word_count = len(word_list)

        data = {
            "sweetspot_completed": sweetspot_completed,
            "dreamjob_completed": dreamjob_completed,
            "word_count": word_count,
        }
        logger.debug(data)

        return Response(UserStatusSerializer(data).data)

class ApiRole(APIView):
    """
    Role as part of the Profession / Role / Attribute
    """
    permission_classes = [AllowAny]

    def get(self, request, id=None, format=None):
        """
        Return Role(s)
        """
        if id:
            msg = "Role: {}".format(id)
        else:
            msg = "Role listing"
        logger.debug(msg)
        try:
            if id:
                data = Role.objects.get(pk=id)
            else:
                data = Role.objects.all()
        except Role.DoesNotExist:
            raise Http404

        if id:
            return Response(RoleSerializer(data).data)
        else:
            return Response(RoleSerializer(data, many=True).data)

class ApiProfession(APIView):
    """
    Professions as part of the Profession / Role / Attribute
    """
    permission_classes = [AllowAny]

    def get(self, request, id=None, format=None):
        """
        Return Profession(s)
        """
        if id:
            msg = "Profession: {}".format(id)
        else:
            msg = "Profession listing"
        logger.debug(msg)
        try:
            if id:
                data = Profession.objects.get(pk=id)
            else:
                data = Profession.objects.all()
        except Profession.DoesNotExist:
            raise Http404

        if id:
            return Response(ProfessionSerializer(data).data)
        else:
            return Response(ProfessionSerializer(data, many=True).data)

class ApiTypeAttributes(APIView):
    """
    TypeAttributes as part of the Profession / Role / Attribute
    """
    permission_classes = [AllowAny]

    def get(self, request, id=None, format=None):
        """
        Return TypeAttributes(s)
        """
        if id:
            msg = "TypeAttributes: {}".format(id)
        else:
            msg = "TypeAttributes listing"
        logger.debug(msg)
        try:
            if id:
                data = TypeAttributes.objects.get(pk=id)
            else:
                data = TypeAttributes.objects.all()
        except TypeAttributes.DoesNotExist:
            raise Http404

        if id:
            return Response(TypeAttributesSerializer(data).data)
        else:
            return Response(TypeAttributesSerializer(data, many=True).data)

class ApiTypeAttributesRoles(APIView):
    """
    TypeAttributes as part of the Profession / Role / Attribute
    """
    permission_classes = [AllowAny]

    def get(self, request, id=None, format=None):
        """
        Return roles with the given TypeAttribute
        """
        if id:
            msg = "TypeAttribute roles: {}".format(id)
        else:
            raise Http404
        logger.debug(msg)
        try:
            ta = TypeAttributes.objects.get(pk=id)
            data = Role.objects.filter(attributes=ta)
        except TypeAttributes.DoesNotExist:
            raise Http404

        return Response(RoleSerializer(data, many=True).data)

class ApiVersion(APIView):
    """
    Version
    """
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Return version information
        """
        prod = None
        if settings.BUILD_CONFIG == "PROD":
            prod = True
        else:
            prod = False
        version = "{}.{}.{}-{}".format(
            settings.VERSION_MAJOR,
            settings.VERSION_MINOR,
            settings.VERSION_REVISION,
            settings.BUILD_CONFIG.lower(),
        )
        data = {
            'major': settings.VERSION_MAJOR,
            'minor': settings.VERSION_MINOR,
            'revision': settings.VERSION_REVISION,
            'version': version,
            'production': prod,
        }

        return Response(VersionSerializer(data).data)
