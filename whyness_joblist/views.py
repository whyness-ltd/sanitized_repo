#----------------------------------------------------------------------
# Whyness job list views
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
from django.shortcuts import render

import logging

from django.http import Http404, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from whyness_django.views import get_auth_user
from whyness_django.views import tracker_log, get_host_info
from whyness_django.models import AuthUser

from whyness_joblist.models import Company
from whyness_joblist.models import Job
from whyness_joblist.models import JobList
from whyness_joblist.models import JobShow
from whyness_joblist.models import JobStatus

from whyness_joblist.serializers import JobListSerializer
from whyness_joblist.serializers import JobShowSerializer
from whyness_joblist.serializers import JobStatusSerializer

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from whyness_django.models import STATUS_ACTIVE

logger = logging.getLogger(__name__)

class ApiList(APIView):
    """Return a personalised list of jobs"""
    permission_classes = [AllowAny]

    def get(self, request, filter=None, format=None):
        """
        Return list of jobs for a user
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        job_status_id = -1
        if filter:
            if filter.lower() == 'unseen':
                job_status_id = 0
            elif filter.lower() == 'seen':
                job_status_id = 1
            elif filter.lower() == 'liked':
                job_status_id = 2
            elif filter.lower() == 'rejected':
                job_status_id = 3
            elif filter.lower() == 'applied':
                job_status_id = 4

        tracker_log(
            activity='joblist_list',
            request=request,
            user=user,
        )

        # TODO Add user filter
        # TODO Filter out rejected
        sql_select = """
        SELECT
            job.id AS id,
            job.job_id AS job_id,
            job.job_id AS job_ref,
            company.id AS company_id,
            company.name AS company,
            company.website AS company_website,
            company.logo,
            job.title,
            country.name AS country,
            job.location,
            job.job_type,
            job.job_link,
            CASE status.status
                WHEN 1 THEN 'SEEN'
                WHEN 2 THEN 'LIKED'
                WHEN 3 THEN 'REJECTED'
                WHEN 4 THEN 'APPLIED'
                ELSE 'UNSEEN'
            END AS status
        FROM whyness_joblist_job AS job
        INNER JOIN whyness_joblist_company AS company
        ON job.company_id = company.id
        INNER JOIN whyness_joblist_country AS country
        ON job.country_id = country.id
        LEFT OUTER JOIN whyness_joblist_jobstatus AS status
        ON job.id = status.job_id
        AND status.user_id = %s
        """
        sql_where = """
        WHERE job.status = 1
        """
        sql_order = """
        ORDER BY job.create_date
        """

        if job_status_id:
            msg = 'job_status_id'
        else:
            msg = 'not job_status_id'
        logger.debug(msg)

        if job_status_id > 0:
            sql_extra = """
            AND status.status = %s
            """
            sql = sql_select + sql_where + sql_extra + sql_order
            data = JobList.objects.raw(sql, [user.id, job_status_id])
        elif job_status_id > -1:
            # Special handling for Job status == 0 as status may be either
            # zero (0) or not there (null)
            sql_extra = """
            AND (status.status IS NULL
            OR status.status = 0)
            """
            sql = sql_select + sql_where + sql_extra + sql_order
            data = JobList.objects.raw(sql, [user.id])
        else:
            sql = sql_select + sql_where + sql_order
            data = JobList.objects.raw(sql, [user.id])

        return Response(JobListSerializer(data, many=True).data)

class ApiJob(APIView):
    """Return a job"""
    permission_classes = [AllowAny]

    def get(self, request, id=None, format=None):
        """
        Return list of jobs, optionally filtered by status
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='joblist_job',
            request=request,
            user=user,
        )

        try:
            # Get the job if it's still available
            # TODO If someone has applied, perhaps they should
            # be able to view the job
            job = Job.objects.get(id=id, status=STATUS_ACTIVE)
        except Job.DoesNotExist as err:
            msg = "Job is not available: {}".format(err)
            logger.warning(msg)
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        sql = """
        SELECT
            job.id,
            job.job_id,
            job.job_id as job_ref,
            company.id AS company_id,
            company.name AS company,
            company.website AS company_website,
            company.logo,
            job.title,
            country.name AS country,
            industry.name AS industry,
            job.location,
            job.job_type,
            job.usp,
            company.values1,
            company.values2,
            company.values3,
            company.values4,
            company.values5,
            job.ssvalues1,
            job.ssvalues2,
            job.ssvalues3,
            job.ssvalues4,
            job.ssvalues5,
            job.strength1,
            job.strength2,
            job.strength3,
            job.impact1,
            job.impact2,
            job.impact3,
            job.skills,
            job.development,
            job.culture,
            job.edi_score,
            job.glassdoor_rating,
            job.job_link,
            job.eligibility,
            CASE status.status
                WHEN 1 THEN 'SEEN'
                WHEN 2 THEN 'LIKED'
                WHEN 3 THEN 'REJECTED'
                WHEN 4 THEN 'APPLIED'
                ELSE 'UNSEEN'
            END AS status,
            job.create_date
        FROM whyness_joblist_job AS job
        INNER JOIN whyness_joblist_company AS company
        ON job.company_id = company.id
        INNER JOIN whyness_joblist_country AS country
        ON job.country_id = country.id
        INNER JOIN whyness_joblist_industry AS industry
        ON job.industry_id = industry.id
        LEFT OUTER JOIN whyness_joblist_jobstatus AS status
        ON job.id = status.job_id
        AND status.user_id = %s
        WHERE job.status = 1
        ORDER BY job.create_date
        """

        data = JobShow.objects.raw(sql, [user.id])[0]

        return Response(JobShowSerializer(data).data)

    def put(self, request, id=None, format=None):
        """
        Updates a user's job status
        """
        job_status = None
        user = get_auth_user(request)
        if not user:
            content = {'message': 'Please authenticate before updating your status'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        tracker_log(
            activity='joblist_job',
            request=request,
            user=user,
        )

        job = None
        try:
            # Get the job if it's still available
            # TODO If someone has applied, perhaps they should
            # be able to change status
            job = Job.objects.get(id=id, status=STATUS_ACTIVE)
        except Job.DoesNotExist as err:
            msg = "Unable to update job status as it is no longer available: {}".format(err)
            logger.warning(msg)
            msg = "Unable to update job status as it is no longer available"
            content = {'error': msg}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            msg = "Unable to get job to update status: {}".format(err)
            logger.warning(msg)
            msg = "Unable to update job status, sorry."
            content = {'error': msg}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            # Get job status status
            job_status = JobStatus.objects.get(user=user, job=job)
        except JobStatus.DoesNotExist as err:
            job_status = JobStatus(user=user, job=job)
        except Exception as err:
            msg = "An Error occured creating job status: {}".format(err)
            logger.error(msg)
            msg = "Unable to get job status, sorry. Please try later"
            content = {'error': msg}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        msg = "Hello job status"
        logger.debug(msg)

        try:
            status_string = request.data['status']
            status_string = status_string.lower()
        except Exception as err:
            msg = "Status not supplied: {}".format(err)
            logger.warning(msg)
            msg = "Please supply the status"
            content = {'error': msg}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if status_string == 'unseen':
            job_status_id = 0
        elif status_string == 'seen':
            job_status_id = 1
        elif status_string == 'liked':
            job_status_id = 2
        elif status_string == 'rejected':
            job_status_id = 3
        elif status_string == 'applied':
            job_status_id = 4
        else:
            msg = "Please supply a valid status"
            content = {'error': msg}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        msg = "Hello job status: {}".format(job_status_id)
        logger.debug(msg)
        try:
            job_status.status = job_status_id
            job_status.save()
        except Exception as err:
            msg = "An Error occured saving job status: {}".format(err)
            logger.error(msg)
            msg = "Unable to update job status, sorry. Please try later"
            content = {'error': msg}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        msg = "Status updated"
        content = {'message': msg}
        return Response(content)
