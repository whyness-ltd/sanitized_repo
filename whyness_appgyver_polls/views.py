#----------------------------------------------------------------------
# Whyness AppGyver poll views
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
import logging

from django.shortcuts import render
from django.http import Http404

from whyness_django.views import get_auth_user, get_host_info, get_useragent
from whyness_django.views import tracker_log

from whyness_appgyver_polls.models import DreamJob
from whyness_appgyver_polls.models import SweetSpotValue
from whyness_appgyver_polls.models import SweetSpotStrength
from whyness_appgyver_polls.models import SweetSpotImpact
from whyness_appgyver_polls.models import SweetSpot
from whyness_appgyver_polls.models import STATUS_ACTIVE
from whyness_appgyver_polls.serializers import DreamJobSerializer
from whyness_appgyver_polls.serializers import SweetSpotValueSerializer
from whyness_appgyver_polls.serializers import SweetSpotStrengthSerializer
from whyness_appgyver_polls.serializers import SweetSpotImpactSerializer
from whyness_appgyver_polls.serializers import SweetSpotSerializer

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

class ApiDreamJob(APIView):
    """
    Manage DreamJob polls
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, id=None, format=None):
        """
        Return dream job
        """
        user = get_auth_user(request)
        if user:
            msg = "UserID: {}".format(user.id)
            logger.debug(msg)
        else:
            pass
            #raise Http404

        tracker_log(
            activity='dreamjob',
            request=request,
            user=user,
        )

        if id:
            msg = "DreamJob: {}".format(id)
        else:
            msg = "DreamJob listing"
        logger.debug(msg)
        try:
            if id:
                data = DreamJob.objects.get(user=user, pk=id)
            else:
                data = DreamJob.objects.filter(user=user).order_by('-create_date')
        except DreamJob.DoesNotExist:
            raise Http404

        if id:
            return Response(DreamJobSerializer(data).data)
        else:
            return Response(DreamJobSerializer(data, many=True).data)

    def post(self, request, format=None):
        """
        Store dream job poll
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='dreamjob',
            request=request,
            user=user,
        )

        try:
            msg = "Post dream job: {}".format(request.data)
            logger.debug(msg)
        except:
            msg = "Post dream job: None"
            logger.debug(msg)

        try:
            data_response = DreamJobSerializer(data=request.data)
        except Exception as err:
            msg = "An Error occured processing this DreamJob: {}".format(err)
            logger.warning(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        if data_response.is_valid():
            useragent = get_useragent(request)
            (remote_addr, remote_host) = get_host_info(request)
            result = data_response.save(user=user, ip=remote_addr, useragent=useragent)
        else:
            return Response(data_response.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(DreamJobSerializer(result).data)

    def put(self, request, id=None, format=None):
        """
        Store poll
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='dreamjob',
            request=request,
            user=user,
        )

        (remote_addr, remote_host) = get_host_info(request)

        msg = "Put dream job: {}".format(
            request.data,
        )
        logger.debug(msg)

        try:
            if id:
                data = DreamJob.objects.get(user=user, pk=id)
                data_response = DreamJobSerializer(data, data=request.data)
            else:
                data_response = DreamJobSerializer(data=request.data)
        except Exception as err:
            msg = "An Error occured processing this DreamJob: {}".format(err)
            logger.warning(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        if data_response.is_valid():
            useragent = get_useragent(request)
            (remote_addr, remote_host) = get_host_info(request)
            result = data_response.save(user=user, ip=remote_addr, useragent=useragent)
        else:
            return Response(data_response.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(DreamJobSerializer(result).data)

class ApiSweetSpotValue(APIView):
    """
    Manage Sweet spot values
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    def get(self, request, id=None, format=None):
        """
        Return sweet spot values
        """
        if id:
            msg = "SweetSpotValue: {}".format(id)
        else:
            msg = "SweetSpotValue listing"
        logger.debug(msg)
        try:
            if id:
                data = SweetSpotValue.objects.get(
                    status=STATUS_ACTIVE,
                    pk=id
                )
            else:
                data = SweetSpotValue.objects.filter(
                    status=STATUS_ACTIVE
                ).order_by('title')
        except SweetSpotValue.DoesNotExist:
            raise Http404

        if id:
            return Response(SweetSpotValueSerializer(data).data)
        else:
            return Response(SweetSpotValueSerializer(data, many=True).data)

class ApiSweetSpotStrength(APIView):
    """
    Manage sweet spot strengths
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    def get(self, request, id=None, format=None):
        """
        Return sweet spot strengths
        """
        if id:
            msg = "SweetSpotStrength: {}".format(id)
        else:
            msg = "SweetSpotStrength listing"
        logger.debug(msg)
        try:
            if id:
                data = SweetSpotStrength.objects.get(
                    status=STATUS_ACTIVE,
                    pk=id
                )
            else:
                data = SweetSpotStrength.objects.filter(
                    status=STATUS_ACTIVE
                ).order_by('title')
        except SweetSpotStrength.DoesNotExist:
            raise Http404

        if id:
            return Response(SweetSpotStrengthSerializer(data).data)
        else:
            return Response(SweetSpotStrengthSerializer(data, many=True).data)

class ApiSweetSpotImpact(APIView):
    """
    Manage sweet spot values
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    def get(self, request, id=None, format=None):
        """
        Return sweet spot impact
        """
        if id:
            msg = "SweetSpotImpact: {}".format(id)
        else:
            msg = "SweetSpotImpact listing"
        logger.debug(msg)
        try:
            if id:
                data = SweetSpotImpact.objects.get(
                    status=STATUS_ACTIVE,
                    pk=id
                )
            else:
                data = SweetSpotImpact.objects.filter(
                    status=STATUS_ACTIVE
                ).order_by('title')
        except SweetSpotImpact.DoesNotExist:
            raise Http404

        if id:
            return Response(SweetSpotImpactSerializer(data).data)
        else:
            return Response(SweetSpotImpactSerializer(data, many=True).data)

class ApiSweetSpot(APIView):
    """
    Manage SweetSpot polls
    """
    permission_classes = [AllowAny]

    def get(self, request, id=None, format=None):
        """
        Return dream job
        """
        user = get_auth_user(request)
        if user:
            msg = "UserID: {}".format(user.id)
            logger.debug(msg)
        else:
            pass
            #raise Http404

        tracker_log(
            activity='sweetspot',
            request=request,
            user=user,
        )

        if id:
            msg = "SweetSpot: {}".format(id)
        else:
            msg = "SweetSpot listing"
        logger.debug(msg)
        try:
            if id:
                data = SweetSpot.objects.get(user=user, pk=id)
            else:
                data = SweetSpot.objects.filter(user=user).order_by('-create_date')
        except SweetSpot.DoesNotExist:
            raise Http404

        if id:
            return Response(SweetSpotSerializer(data).data)
        else:
            return Response(SweetSpotSerializer(data, many=True).data)

    def post(self, request, id=None, format=None):
        """
        Create a new sweet spot poll
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='sweetspot',
            request=request,
            user=user,
        )

        (remote_addr, remote_host) = get_host_info(request)

        try:
            msg = "Post sweet spot: {}".format(
                request.data,
            )
        except Exception as err:
            msg = "Post sweet spot failed: {}".format(err)
        logger.debug(msg)

        try:
            if id:
                msg = "Updating sweet spot: {}".format(id)
                logger.debug(msg)
                instance_data = SweetSpot.objects.get(pk=id, user=user)
                data_response = SweetSpotSerializer(
                    instance_data,
                    data=request.data
                )
            else:
                msg = "Creating a new sweet spot"
                logger.debug(msg)
                data_response = SweetSpotSerializer(data=request.data)
        except Exception as err:
            msg = "An Error occured processing this SweetSpot: {}".format(err)
            logger.warning(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        if data_response.is_valid():
            useragent = get_useragent(request)
            (remote_addr, remote_host) = get_host_info(request)
            result = data_response.save(user=user, ip=remote_addr, useragent=useragent)
            logger.debug(result)
        else:
            logger.debug(data_response.errors)
            return Response(data_response.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(SweetSpotSerializer(result).data)

    def put(self, request, id=None, format=None):
        """
        Store sweet spot poll
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='sweetspot',
            request=request,
            user=user,
        )

        (remote_addr, remote_host) = get_host_info(request)

        msg = "Put sweet spot: {}".format(
            request.data,
        )
        logger.debug(msg)

        try:
            if id:
                msg = "Updating sweet spot: {}".format(id)
                logger.debug(msg)
                instance_data = SweetSpot.objects.get(pk=id, user=user)
                data_response = SweetSpotSerializer(
                    instance_data,
                    data=request.data
                )
            else:
                msg = "Creating a new sweet spot"
                logger.debug(msg)
                data_response = SweetSpotSerializer(data=request.data)
        except Exception as err:
            msg = "An Error occured processing this SweetSpot: {}".format(err)
            logger.warning(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        if data_response.is_valid():
            useragent = get_useragent(request)
            (remote_addr, remote_host) = get_host_info(request)
            result = data_response.save(user=user, ip=remote_addr, useragent=useragent)
            logger.debug(result)
        else:
            logger.debug(data_response.errors)
            return Response(data_response.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(SweetSpotSerializer(result).data)
