#----------------------------------------------------------------------
# Whyness prospects views
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

import logging

from django.shortcuts import render
from django.http import Http404

from whyness_prospect.models import Prospect

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from whyness_prospect.serializers import ProspectSerializer

logger = logging.getLogger(__name__)

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

def prospect_index(request):
    try:
        prospects = Prospect.objects.all()
    except Exception as err:
        msg = 'Error finding Prospects: {}'.format(err)
        logger.error(msg)
    context = {
        "prospects": prospects,
    }
    return render(request, 'whyness_prospect/prospect_index.html', context)

def prospect(request, id):
    try:
        prospect = Prospect.objects.get(pk=id)
    except ObjectDoesNotExist as err:
        # No Prospect with that id
        msg = 'Prospect not found for: {}: {}'.format(id, err)
        logger.debug(msg)
    except Exception as err:
        msg = 'Error finding Prospect: {}: {}'.format(id, err)
        logger.error(msg)
    context = {
        "prospect": prospect,
    }
    return render(request, 'whyness_prospect/prospect.html', context)

class ApiProspect(APIView):
    """
    Manage Prospects
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    def get(self, request, id=None, email=None):
        """
        Return prospect
        """
        if id:
            msg = "Prospect: {}".format(id)
        elif email:
            msg = "Prospect: {}".format(email)
        else:
            msg = "Prospect listing"
        logger.debug(msg)
        try:
            if id:
                prospect = Prospect.objects.get(pk=id)
            elif email:
                prospect = Prospect.objects.get(email=email)
            else:
                prospect = Prospect.objects.all().order_by('-create_date')
        except Prospect.DoesNotExist:
            raise Http404

        if id or email:
            return Response(ProspectSerializer(prospect).data)
        else:
            return Response(ProspectSerializer(prospect, many=True).data)

    def put(self, request, format=None):
        """
        Store media
        """
        (remote_addr, remote_host) = get_host_info(request)

        msg = "Put media: {}".format(
            request.query_params,
        )
        logger.debug(msg)

        try:
            prospect = ProspectSerializer(data=request.data)
        except Exception as err:
            msg = "An Error occured processing this prospect: {}".format(err)
            logger.warning(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        msg = "Prospect: {}".format(prospect)
        logger.debug(msg)

        if prospect.is_valid():
            (remote_addr, remote_host) = get_host_info(request)
            prospect.update_ip = remote_addr
            msg = "Prospect response is valid"
            logger.debug(msg)
            result = prospect.save()
        else:
            return Response(prospect.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProspectSerializer(result).data)

    def delete(self, request, id=None, email=None, format=None):
        """
        Delete Prospect
        """
        errors = {}
        (remote_addr, remote_host) = get_host_info(request)
        msg = "Delete ?"
        prospect = None
        if id:
            try:
                prospect = Prospect.objects.get(pk=id)
                prospect.delete()
                msg = "__name__:Prospect.delete: {}: {}: {} <{}>".format(
                    id,
                    prospect.name,
                    prospect.email,
                    'Prospect deleted'
                )
                logger.debug(msg)
            except Prospect.DoesNotExist:
                msg = "__name__:Prospect.delete: {}: {}: {}".format(id, '404', 'Prospect does not exist')
                logger.error(msg)
                raise Http404
            msg = "Delete prospect: {}".format(id)
        elif email:
            msg = "Delete prospect: {}".format(email)
            try:
                prospect = Prospect.objects.get(email=email)
                prospect.delete()
                msg = "__name__:Prospect.delete: {}: {}: {} <{}>".format(
                    id,
                    prospect.name,
                    prospect.email,
                    'Prospect deleted'
                )
                logger.debug(msg)
            except Prospect.DoesNotExist:
                msg = "__name__:Prospect.delete: {}: {}: {}".format(id, '404', 'Prospect does not exist')
                logger.error(msg)
                raise Http404
        if not prospect:
            errors = '{"prospect": ["An id or email is required"]}'
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
