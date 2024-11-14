#----------------------------------------------------------------------
# Whyness errorlog forms
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

"""
"""

import os
import logging
from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminTextInputWidget
from whyness_error.models import ErrorLog

logger = logging.getLogger(__name__)

class ErrorLogForm(ModelForm):
    class Meta:
        model = ErrorLog
        fields = [
            'errorcode',
            'hostip',
            'useragent',
            'errormessage',
        ]

