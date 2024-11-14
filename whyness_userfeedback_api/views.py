#----------------------------------------------------------------------
# Whyness User feedback api views
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
import logging

from collections import namedtuple

from firebase_admin import credentials
from firebase_admin import auth

from django.db import connection
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import Http404
from django.shortcuts import render

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from whyness_django.models import AuthUser
from whyness_django.views import get_auth_user
from whyness_django.views import tracker_log

from whyness_userfeedback_api.serializers import UserFeedbackSerializer

logger = logging.getLogger(__name__)

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def userfeedback_values(request):
    """
    Whyness user value feedback
    """
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('home'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('home'))

    # User value feedback
    raw_sql = """
    SELECT
        value, count(value) AS value_count
    FROM (
        SELECT ssv1.title AS value
        FROM whyness_userfeedback_sweetspot AS ss
        INNER JOIN whyness_userfeedback_sweetspotvalue AS ssv1
        ON ss.value1_id = ssv1.id

        UNION ALL

        SELECT ssv2.title
        FROM whyness_userfeedback_sweetspot AS ss
        INNER JOIN whyness_userfeedback_sweetspotvalue AS ssv2
        ON ss.value2_id = ssv2.id

        UNION ALL

        SELECT ssv3.title
        FROM whyness_userfeedback_sweetspot AS ss
        INNER JOIN whyness_userfeedback_sweetspotvalue AS ssv3
        ON ss.value3_id = ssv3.id
    ) AS ss
    GROUP BY value
    ORDER BY 2 DESC, value
    """
    with connection.cursor() as cursor:
        cursor.execute(raw_sql)
        values = namedtuplefetchall(cursor)
    context = {
        "values": values,
    }
    template = 'whyness_userfeedback_api/userfeedback-value.html'
    return render(request, template, context)

def userfeedback_strengths(request):
    """
    Whyness user strength feedback
    """
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('home'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('home'))

    #Strengths
    raw_sql = """
    SELECT strength, count(strength) AS strength_count
    FROM (
        SELECT sss1.title AS strength
        FROM whyness_userfeedback_sweetspot AS ss
        INNER JOIN whyness_userfeedback_sweetspotstrength AS sss1
        ON ss.strength1_id = sss1.id

        UNION ALL

        SELECT sss2.title
        FROM whyness_userfeedback_sweetspot AS ss
        INNER JOIN whyness_userfeedback_sweetspotstrength AS sss2
        ON ss.strength2_id = sss2.id

        UNION ALL

        SELECT sss3.title
        FROM whyness_userfeedback_sweetspot AS ss
        INNER JOIN whyness_userfeedback_sweetspotstrength AS sss3
        ON ss.strength3_id = sss3.id
    ) AS ss
    GROUP BY strength
    ORDER BY 2 DESC, strength
    """
    with connection.cursor() as cursor:
        cursor.execute(raw_sql)
        strengths = namedtuplefetchall(cursor)

    context = {
        "strengths": strengths,
    }
    template = 'whyness_userfeedback_api/userfeedback-strength.html'
    return render(request, template, context)

def userfeedback_impacts(request):
    """
    Whyness user impact feedback
    """
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('home'))
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('home'))

    # Impacts
    raw_sql = """
    SELECT impact, count(impact) AS impact_count
    FROM (
        SELECT ssi1.title AS impact
        FROM whyness_userfeedback_sweetspot AS ss
        INNER JOIN whyness_userfeedback_sweetspotimpact AS ssi1
        ON ss.impact1_id = ssi1.id

        UNION ALL

        SELECT ssi2.title
        FROM whyness_userfeedback_sweetspot AS ss
        INNER JOIN whyness_userfeedback_sweetspotimpact AS ssi2
        ON ss.impact2_id = ssi2.id

        UNION ALL

        SELECT ssi3.title
        FROM whyness_userfeedback_sweetspot AS ss
        INNER JOIN whyness_userfeedback_sweetspotimpact AS ssi3
        ON ss.impact3_id = ssi3.id
    ) AS ss
    GROUP BY impact
    ORDER BY 2 DESC, impact
    """
    with connection.cursor() as cursor:
        cursor.execute(raw_sql)
        impacts = namedtuplefetchall(cursor)

    context = {
        "impacts": impacts,
    }
    template = 'whyness_userfeedback_api/userfeedback-impact.html'
    return render(request, template, context)

class ApiUserFeedback(APIView):
    """
    Feedback from friends and colleagues
    """
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Return feedback
        - Values
        - Strength
        - Impacts
        - Confidence
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='api_user_feedback',
            request=request,
            user=user,
        )

        # User value feedback
        raw_sql = """
        SELECT ss.user_id, au.name AS name, au.email AS email,
            value, count(value) AS value_count
        FROM (
            SELECT user_id, ssv1.title AS value
            FROM whyness_userfeedback_sweetspot AS ss
            INNER JOIN whyness_userfeedback_sweetspotvalue AS ssv1
            ON ss.value1_id = ssv1.id

            UNION ALL

            SELECT user_id, ssv2.title
            FROM whyness_userfeedback_sweetspot AS ss
            INNER JOIN whyness_userfeedback_sweetspotvalue AS ssv2
            ON ss.value2_id = ssv2.id

            UNION ALL

            SELECT user_id, ssv3.title
            FROM whyness_userfeedback_sweetspot AS ss
            INNER JOIN whyness_userfeedback_sweetspotvalue AS ssv3
            ON ss.value3_id = ssv3.id
        ) AS ss
        INNER JOIN whyness_django_authuser AS au
        ON ss.user_id = au.id
        WHERE ss.user_id = %s
        GROUP BY
            ss.user_id, au.name, au.email,
            value
        ORDER BY 5 DESC, 4
        """
        with connection.cursor() as cursor:
            cursor.execute(raw_sql, [user.id])
            values = namedtuplefetchall(cursor)
        #Strengths
        raw_sql = """
        SELECT ss.user_id, au.name AS name, au.email AS email,
            strength, count(strength) AS strength_count
        FROM (
            SELECT user_id, sss1.title AS strength
            FROM whyness_userfeedback_sweetspot AS ss
            INNER JOIN whyness_userfeedback_sweetspotstrength AS sss1
            ON ss.strength1_id = sss1.id

            UNION ALL

            SELECT user_id, sss2.title
            FROM whyness_userfeedback_sweetspot AS ss
            INNER JOIN whyness_userfeedback_sweetspotstrength AS sss2
            ON ss.strength2_id = sss2.id

            UNION ALL

            SELECT user_id, sss3.title
            FROM whyness_userfeedback_sweetspot AS ss
            INNER JOIN whyness_userfeedback_sweetspotstrength AS sss3
            ON ss.strength3_id = sss3.id
        ) AS ss
        INNER JOIN whyness_django_authuser AS au
        ON ss.user_id = au.id
        WHERE ss.user_id = %s
        GROUP BY
            ss.user_id, au.name, au.email,
            strength
        ORDER BY 5 DESC, 4
        """
        with connection.cursor() as cursor:
            cursor.execute(raw_sql, [user.id])
            strengths = namedtuplefetchall(cursor)
        # Impacts
        raw_sql = """
        SELECT ss.user_id, au.name AS name, au.email AS email,
            impact, count(impact) AS impact_count
        FROM (
            SELECT user_id, ssi1.title AS impact
            FROM whyness_userfeedback_sweetspot AS ss
            INNER JOIN whyness_userfeedback_sweetspotimpact AS ssi1
            ON ss.impact1_id = ssi1.id

            UNION ALL

            SELECT user_id, ssi2.title
            FROM whyness_userfeedback_sweetspot AS ss
            INNER JOIN whyness_userfeedback_sweetspotimpact AS ssi2
            ON ss.impact2_id = ssi2.id

            UNION ALL

            SELECT user_id, ssi3.title
            FROM whyness_userfeedback_sweetspot AS ss
            INNER JOIN whyness_userfeedback_sweetspotimpact AS ssi3
            ON ss.impact3_id = ssi3.id
        ) AS ss
        INNER JOIN whyness_django_authuser AS au
        ON ss.user_id = au.id
        WHERE ss.user_id = %s
        GROUP BY
            ss.user_id, au.name, au.email,
            impact
        ORDER BY 5 DESC, 4
        """
        with connection.cursor() as cursor:
            cursor.execute(raw_sql, [user.id])
            impacts = namedtuplefetchall(cursor)
        # Confidence
        raw_sql = """
        SELECT ss.user_id, au.name,
            au.email,
            ssvc.title AS valueconfidence,
            COUNT(ssvc.title) AS valueconfidence_count,
            sssc.title AS strengthconfidence,
            COUNT(sssc.title) AS strengthconfidence_count,
            ssic.title AS impactconfidence,
            COUNT(ssic.title) AS impactconfidence_count
        FROM whyness_userfeedback_sweetspot AS ss
        INNER JOIN whyness_django_authuser AS au
        ON ss.user_id = au.id
        INNER JOIN whyness_userfeedback_sweetspotconfidence AS ssvc
        ON ss.valueconfidence_id = ssvc.id
        INNER JOIN whyness_userfeedback_sweetspotconfidence AS sssc
        ON ss.strengthconfidence_id = sssc.id
        INNER JOIN whyness_userfeedback_sweetspotconfidence AS ssic
        ON ss.impactconfidence_id = ssic.id
        WHERE ss.user_id = %s
        GROUP BY
        user_id,
        au.name,
        au.email,
        valueconfidence,
        strengthconfidence,
        impactconfidence"""
        with connection.cursor() as cursor:
            cursor.execute(raw_sql, [user.id])
            confidence = namedtuplefetchall(cursor)

        data = {
            "values": values,
            "strengths": strengths,
            "impacts": impacts,
            "confidence": confidence,
        }

        return Response(UserFeedbackSerializer(data).data)
