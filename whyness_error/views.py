#----------------------------------------------------------------------
# Whyness error views
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

"""
"""
from whyness_django.views import get_host_info
from whyness_django.views import get_useragent

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from whyness_error.serializers import ErrorLogSerializer

class ApiErrorLog(APIView):
    """
    Log errors
    """
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        """
        Create a new error log
        """
        serializer = ErrorLogSerializer(data=request.data)

        (remote_addr, remote_host) = get_host_info(request)
        user_agent = get_useragent(request)

        if serializer.is_valid():
            serializer.save(
                hostip=remote_addr,
                useragent=user_agent,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            msg = 'Request error: ip/name/agent/error {} / {} / {} / {}'.format(
                remote_addr,
                remote_host,
                user_agent,
                request.data,
            )
            logger.info(msg)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
