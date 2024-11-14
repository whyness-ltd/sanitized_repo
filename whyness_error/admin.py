#----------------------------------------------------------------------
# Whyness error admin
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

"""
"""
from django.contrib import admin

from whyness_error.models import ErrorLog
from whyness_error.forms import ErrorLogForm

class ErrorLogAdmin(admin.ModelAdmin):
    form = ErrorLogForm
    fields = (
        'id',
        'create_date',
        'hostip',
        'useragent',
        'errorcode',
        'errormessage',
    )

    readonly_fields = [
        'id',
        'create_date',
        'hostip',
        'useragent',
        'errorcode',
        'errormessage',
    ]
    list_display = [
        'create_date',
        'errorcode',
        'errormessage',
    ]
    ordering = ['-create_date']

admin.site.register(ErrorLog, ErrorLogAdmin)
