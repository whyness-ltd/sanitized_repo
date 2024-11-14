#----------------------------------------------------------------------
# Whyness forms
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
from whyness_django.models import Audio
from django.contrib.staticfiles.storage import staticfiles_storage

logger = logging.getLogger(__name__)

STATUS_INACTIVE = 0
STATUS_ACTIVE = 1

STATUS_CHOICES = (
    (STATUS_INACTIVE, ('Inactive')),
    (STATUS_ACTIVE, ('Active')),
)

class TinyMceWidget(forms.Textarea):
    """
    Setup the JS files and targetting CSS class for a textarea to
    use TinyMCE.
    """

    class Media:
        _tinymce_js = (
            staticfiles_storage.url("js/tinymce/tinymce.min.js"),
            staticfiles_storage.url("js/tinymce_setup.js"),
        )
        js = _tinymce_js

    def __init__(self, *args, **kwargs):
        super(TinyMceWidget, self).__init__(*args, **kwargs)
        self.attrs["class"] = "mceEditor"

class AudioForm(ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=75,
        widget=forms.TextInput(attrs={
            'class':'form-control mceEditor',
            'placeholder':'Title',
            'style': 'width: 500px;'
        }),
        error_messages={'required': 'Please enter the title of the media'},
        required=True,
        help_text='Every media item needs a title',
    )
    media = forms.FileField(
        label='Audio file',
        widget=forms.FileInput(attrs={
            'class':'form-control',
            'placeholder':'File',
        }),
        error_messages={'required': 'Please choose the media'},
        required=True,
        help_text='Media is required',
    )
    status = forms.ChoiceField(
        label='Status',
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES,
        required=False,
        help_text='Status of this audio',
    )
    class Meta:
        model = Audio
        fields = ['title', 'media', 'status', 'user']

class QuestionForm(ModelForm):
    question = forms.CharField(
        label='Question',
        max_length=500,
        widget=forms.TextInput(attrs={
            'class':'form-control mceEditor',
            'placeholder':'Question',
            'style': 'width: 500px;'
        }),
        error_messages={'required': 'Please enter a question'},
        required=True,
    )
    status = forms.ChoiceField(
        label='Status',
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES,
        required=False,
        help_text='Status of this question',
    )
    class Meta:
        model = Audio
        fields = ['question', 'status']
