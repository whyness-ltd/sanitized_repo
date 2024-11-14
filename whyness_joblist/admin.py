#----------------------------------------------------------------------
# Whyness job list admin
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
from django.contrib import admin

from whyness_joblist.models import Country
from whyness_joblist.models import Company
from whyness_joblist.models import Industry
from whyness_joblist.models import Job

class CountryAdmin(admin.ModelAdmin):
    model = Country
    fields = (
        'name',
        'code',
        'code3',
        ('update_date', 'update_ip'),
        'create_date',
    )
    readonly_fields = ['update_ip', 'update_date', 'create_date']
    list_display = [
        'name',
        'code',
        ]
    ordering = ['name',]

class IndustryAdmin(admin.ModelAdmin):
    model = Country
    fields = (
        'name',
        ('update_date', 'update_ip'),
        'create_date',
    )
    readonly_fields = ['update_ip', 'update_date', 'create_date']
    list_display = [
        'name',
        ]
    ordering = ['name',]

class CompanyAdmin(admin.ModelAdmin):
    model = Company
    fields = (
        'name',
        'logo',
        'overview',
        'industry',
        'size',
        'website',
        'email',
        'values1',
        'values2',
        'values3',
        'values4',
        'values5',
        'status',
        ('update_date', 'update_ip'),
        'create_date',
    )
    readonly_fields = ['update_ip', 'update_date', 'create_date']
    list_display = [
        'name',
        ]
    ordering = ['name',]

class JobAdmin(admin.ModelAdmin):
    model = Job
    fields = (
        'job_id',
        'company',
        'title',
        'country',
        'location',
        'job_type',
        'usp',
        'ssvalues1',
        'ssvalues2',
        'ssvalues3',
        'ssvalues4',
        'ssvalues5',
        'strength1',
        'strength2',
        'strength3',
        'strength4',
        'strength5',
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
        'published_date',
        ('update_date', 'update_ip'),
        'create_date',
    )
    readonly_fields = ['update_ip', 'update_date', 'create_date']
    list_display = [
        'id',
        'job_id',
        'company',
        'title',
        'published_date',
        'status',
        ]
    ordering = ['id',]

# Register your models here.
admin.site.register(Country, CountryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Job, JobAdmin)
