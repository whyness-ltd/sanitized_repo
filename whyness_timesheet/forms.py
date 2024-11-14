#----------------------------------------------------------------------
# Whyness Timesheet forms
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

"""
"""

import os
import logging
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ModelForm
from whyness_timesheet.models import Timeentry

logger = logging.getLogger(__name__)

class TimeentryForm(ModelForm):
    hr_recruitment = forms.DecimalField(
        label='Recruitment',
        error_messages={'required': 'Please enter the number of hours worked or zero'},
        required=False,
        help_text='The number of hours is required',
    )
    design_architecture = forms.DecimalField(
        label='Solution Design and Development',
        error_messages={'required': 'Please enter the number of hours worked or zero'},
        required=False,
        help_text='The number of hours is required',
    )
    comms_marketing = forms.DecimalField(
        label='Market / Customer Research & Engagement, & Strategy',
        error_messages={'required': 'Please enter the number of hours worked or zero'},
        required=False,
        help_text='The number of hours is required',
    )
    user_research = forms.DecimalField(
        label='User research and testing',
        error_messages={'required': 'Please enter the number of hours worked or zero'},
        required=False,
        help_text='The number of hours is required',
    )
    annual_leave = forms.DecimalField(
        label='Annual leave',
        error_messages={'required': 'Please enter the number of hours or zero'},
        required=False,
        help_text='The number of hours is required',
    )
    statutory_holiday = forms.DecimalField(
        label='Bank holiday',
        error_messages={'required': 'Please enter the number of hours or zero'},
        required=False,
        help_text='The number of hours is required',
    )
    sick_leave = forms.DecimalField(
        label='Sick leave',
        error_messages={'required': 'Please enter the number of hours or zero'},
        required=False,
        help_text='The number of hours is required',
    )

    sustainability = forms.DecimalField(
        label='Sustainability - do not use',
        error_messages={'required': 'Please enter the number of hours worked or zero'},
        required=False,
        help_text='The number of hours is required',
    )
    functional = forms.DecimalField(
        label='Functional - do not use',
        error_messages={'required': 'Please enter the number of hours worked or zero'},
        required=False,
        help_text='The number of hours is required',
    )
    admin_pmo = forms.DecimalField(
        label='Admin PMO Financial - do not use',
        error_messages={'required': 'Please enter the number of hours worked or zero'},
        required=False,
        help_text='The number of hours is required',
    )
    product_development = forms.DecimalField(
        label='Product development (tech) - do not use',
        error_messages={'required': 'Please enter the number of hours worked or zero'},
        required=False,
        help_text='The number of hours is required',
    )
    strategy = forms.DecimalField(
        label='Business strategy - do not use',
        error_messages={'required': 'Please enter the number of hours worked or zero'},
        required=False,
        help_text='The number of hours is required',
    )
    class Meta:
        model = Timeentry
        fields = [
            'user',
            'date',
            'hr_recruitment',
            'design_architecture',
            'comms_marketing',
            'user_research',
            'annual_leave',
            'statutory_holiday',
            'sick_leave',

            'sustainability',
            'functional',
            'admin_pmo',
            'product_development',
        ]
