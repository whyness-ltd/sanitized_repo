#----------------------------------------------------------------------
# Whyness Machine Learning views
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
import logging
import os
import boto3

from django.conf import settings
from django.shortcuts import render
from django.http import Http404

from whyness_django.models import Audio
from whyness_django.models import TRANSCRIPT_STATUS_DELETED

from whyness_django.views import get_auth_user, get_host_info, get_useragent
from whyness_django.views import tracker_log

from whyness_ml_models.models import MBTI
from whyness_ml_models.serializers import MBTISerializer

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

class ApiMBTI(APIView):
    """
    Available Questions
    """
    permission_classes = [AllowAny]

    def get(self, request, id=None, format=None):
        """
        Return a user's latest MBTI score
        """
        msg = "__name__.ApiMBTI: {}".format(id)
        logger.debug(msg)
        user = get_auth_user(request)
        if user:
            msg = "UserID: {}".format(user.id)
            logger.debug(msg)
        else:
            raise Http404

        data = None
        if id:
            msg = "MBTI: {}".format(id)
        else:
            msg = "MBTI latest"
        logger.debug(msg)

        try:
            if id:
                data = MBTI.objects.get(user=user, pk=id)
            else:
                data = MBTI.objects.filter(user=user).order_by('id')[:1][0]
        except Audio.DoesNotExist:
            raise Http404
        except IndexError:
            data = MBTI()

        stories = ""
        audios = Audio.objects.filter(
            user=user,
            status__lte=TRANSCRIPT_STATUS_DELETED,
        )
        for audio in audios:
            stories = "{} {}".format(stories, audio.transcript)
        word_list = stories.split()
        data.word_count = len(word_list)

        return Response(MBTISerializer(data).data)

