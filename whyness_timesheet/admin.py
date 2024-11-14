#----------------------------------------------------------------------
# Whyness Timesheet admin
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from django.contrib import admin
from django.urls import path

# Register your models here.
from django.contrib import admin

from whyness_timesheet.models import Timeentry

class TimeentryAdmin(admin.ModelAdmin):
    model = Timeentry
    fields = (
        'user', 'date',
        'hr_recruitment',
        'design_architecture',
        'comms_marketing',
        'user_research',
        'annual_leave',
        'statutory_holiday',
        'sick_leave',
        ('update_date', 'update_user'),
        'create_date',
    )
    readonly_fields = ['update_user', 'update_date', 'create_date']
    list_filter = ['date', 'user']
    date_hierarchy = 'date'
    list_display = [
        'user', 'date',
        'total',
        'hr_recruitment',
        'design_architecture',
        'comms_marketing',
        'user_research',
        'annual_leave',
        'statutory_holiday',
        'sick_leave',
        ]
    ordering = ['-date',]

    def save_model(self, request, obj, form, change):
        obj.update_user = request.user
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Timeentry, TimeentryAdmin)
