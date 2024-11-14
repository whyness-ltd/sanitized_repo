#----------------------------------------------------------------------
# Whyness User feedback forms
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

"""
"""

import os

from django import forms
from django.forms import ModelForm

from whyness_userfeedback.models import SweetSpotValue
from whyness_userfeedback.models import SweetSpotStrength
from whyness_userfeedback.models import SweetSpotImpact
from whyness_userfeedback.models import SweetSpotConfidence
from whyness_userfeedback.models import SweetSpot

STATUS_INACTIVE = 0
STATUS_ACTIVE = 1

STATUS_CHOICES = (
    (STATUS_INACTIVE, ('Inactive')),
    (STATUS_ACTIVE, ('Active')),
)

SORT_FIRST = 0
SORT_NORMAL = 1
SORT_LAST = 99
SORT_CHOICES = (
    (SORT_FIRST, ('First')),
    (SORT_NORMAL, ('Normal')),
    (SORT_LAST, ('Last')),
)

class SweetSpotValueForm(ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control mceEditor',
            'placeholder':'Title',
        }),
        error_messages={'required': 'Please enter a title for the sweet spot value'},
        required=True,
        help_text='Every Sweet value spot needs a title',
    )
    sort_order = forms.ChoiceField(
        label='Sort',
        widget=forms.RadioSelect(),
        choices=SORT_CHOICES,
        required=False,
    )
    status = forms.ChoiceField(
        label='Status',
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES,
        required=False,
    )
    class Meta:
        model = SweetSpotValue
        fields = ['title', 'sort_order', 'status', ]

class SweetSpotStrengthForm(ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control mceEditor',
            'placeholder':'Title',
        }),
        error_messages={'required': 'Please enter a title for the sweet spot value'},
        required=True,
        help_text='Every Sweet value spot needs a title',
    )
    sort_order = forms.ChoiceField(
        label='Sort',
        widget=forms.RadioSelect(),
        choices=SORT_CHOICES,
        required=False,
    )
    status = forms.ChoiceField(
        label='Status',
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES,
        required=False,
        help_text='Status of this attribute',
    )
    class Meta:
        model = SweetSpotStrength
        fields = ['title', 'sort_order', 'status', ]

class SweetSpotImpactForm(ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control mceEditor',
            'placeholder':'Title',
        }),
        error_messages={'required': 'Please enter a title for the sweet spot impact'},
        required=True,
        help_text='Every Sweet impact spot needs a title',
    )
    sort_order = forms.ChoiceField(
        label='Sort',
        widget=forms.RadioSelect(),
        choices=SORT_CHOICES,
        required=False,
    )
    status = forms.ChoiceField(
        label='Status',
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES,
        required=False,
        help_text='Status of this attribute',
    )
    class Meta:
        model = SweetSpotImpact
        fields = ['title', 'sort_order', 'status', ]

class SweetSpotConfidenceForm(ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control mceEditor',
            'placeholder':'Title',
        }),
        error_messages={'required': 'Please enter a confidence for the sweet spot'},
        required=False,
        help_text='Every Sweet value spot needs a title',
    )
    sort_order = forms.ChoiceField(
        label='Sort',
        widget=forms.RadioSelect(),
        choices=SORT_CHOICES,
        required=False,
    )
    status = forms.ChoiceField(
        label='Status',
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES,
        required=False,
        help_text='Status of this audio',
    )
    class Meta:
        model = SweetSpotConfidence
        fields = ['title', 'sort_order', 'status', ]

class SweetSpotForm(ModelForm):
    class Meta:
        model = SweetSpot
        fields = [
            'value1', 'value2', 'value3', 'valueother', 'valueconfidence',
            'strength1', 'strength2', 'strength3', 'strengthother', 'strengthconfidence',
            'impact1', 'impact2', 'impact3', 'impactother', 'impactconfidence',
        ]
        labels = {
            'value1': "Primary value",
            'value2': "Secondary value",
            'value3': "Tertiary value",
            'valueother': "Value not listed (optional)",
            'valueconfidence': "Confidence",
            'strength1': "Primary strength",
            'strength2': "Secondary strength",
            'strength3': "Tertiary strength",
            'strengthother': "Strength not listed (optional)",
            'strengthconfidence': "Confidence",
            'impact1': "Primary impact",
            'impact2': "Secondary impact",
            'impact3': "Tertiary impact",
            'impactother': "Impact not listed (optional)",
            'impactconfidence': "Confidence",
        }

