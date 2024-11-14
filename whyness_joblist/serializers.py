#----------------------------------------------------------------------
# Whyness Job listing serializers
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from rest_framework import serializers

from whyness_joblist.models import Company
from whyness_joblist.models import Job
from whyness_joblist.models import JobList
from whyness_joblist.models import JobShow
from whyness_joblist.models import JobStatus

class JobListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobList
        fields = [
            'id',
            'job_id',
            'job_ref',
            'company_id',
            'company',
            'company_website',
            'logo',
            'title',
            'country',
            'location',
            'job_type',
            'job_link',
            'status',
        ]

class JobShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobShow
        fields = [
            'id',
            'job_id',
            'job_ref',
            'company',
            'company_website',
            'logo',
            'title',
            'country',
            'industry',
            'location',
            'job_type',
            'usp',
            'values1',
            'values2',
            'values3',
            'values4',
            'values5',
            'ssvalues1',
            'ssvalues2',
            'ssvalues3',
            'ssvalues4',
            'ssvalues5',
            'strength1',
            'strength2',
            'strength3',
            'impact1',
            'impact2',
            'impact3',
            'skills',
            'development',
            'culture',
            'edi_score',
            'glassdoor_rating',
            'job_link',
            'eligibility',
            'status',
            'create_date',
        ]

class JobStatusSerializer(serializers.Serializer):
    id = serializers.CharField(allow_blank=True)
    job = serializers.CharField(allow_blank=True)
    status = serializers.CharField(allow_blank=True)
    create_date = serializers.CharField(allow_blank=True)
    class Meta:
        fields = [
            'id',
            'job',
            'status',
            'create_date',
        ]
