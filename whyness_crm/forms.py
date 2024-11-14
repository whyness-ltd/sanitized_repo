#----------------------------------------------------------------------
# Whyness crm forms
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
import os
import logging
from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminTextInputWidget
from whyness_crm.models import Message
from whyness_crm.models import TrackerDestination
from whyness_crm.models import UserSQL

from whyness_crm.models import CONTACT_CHOICES

logger = logging.getLogger(__name__)

STATUS_INACTIVE = 0
STATUS_ACTIVE = 1

STATUS_CHOICES = (
    (STATUS_INACTIVE, ('Inactive')),
    (STATUS_ACTIVE, ('Active')),
)

class ContactForm(ModelForm):
    name = forms.CharField(
        label='Name',
        max_length=75,
        widget=forms.TextInput(),
        error_messages={'required': 'Please enter the name of the contact'},
        required=True,
        help_text='Users need a name',
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(),
        required=False,
    )
    use_email = forms.BooleanField(
        label='Email',
        required=False,
        help_text='Tick this box if a user wants to recieve emails',
    )
    is_prospect = forms.BooleanField(
        label='Prospect',
        required=False,
        help_text='Tick this box if the contact is a prospect',
    )
    is_registered = forms.BooleanField(
        label='Registered',
        required=False,
        help_text='Tick this box if the contact is a registered user',
    )
    release = forms.IntegerField(
        label='Release',
        required=False,
    )
    class Meta:
        model = Message
        fields = [
            'title',
            'is_email',
            'release',
            'status',
            'message_html',
            'from_user'
        ]

class MessageForm(ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=75,
        widget=forms.TextInput(attrs={
            'class':'vLargeTextField',
            'placeholder':'Title'
        }),
        error_messages={'required': 'Please enter a title'},
        required=True,
        help_text='The Title is used as the email Subject',
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={
            'class':'form-control TinyEditor',
            'style':'width:100%',
        }),
        error_messages={'required': 'Please enter a description of the data set'},
        required=True,
    )
    message_html = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={
            'class':'form-control TinyEditor',
            'style':'width:100%',
            'placeholder':'Title',
        }),
        error_messages={'required': 'Please enter a message'},
        required=True,
        help_text=(
            'To insert a name use {{ user.name }}<br/>'
            'To insert a clickable link {% crm_link &quot;https://REMOVED %}<br/>'
            'To insert a clickable link with a title {% crm_link &quot;https://REMOVED &quot;title&quot; %}'
        ),
    )
    is_email = forms.BooleanField(
        label='Email',
        required=False,
    )
    status = forms.ChoiceField(
        label='Status',
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES,
        required=False,
        help_text='Status of this message',
    )
    class Meta:
        model = Message
        fields = ['title', 'is_email', 'status', 'message_html', 'from_user']

class UserSQLForm(ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'vLargeTextField',
            'placeholder':'Title'
        }),
        error_messages={'required': 'Please enter the User SQL title'},
        required=True,
        help_text='The title will be used to identify which sql to use',
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={
            'class':'form-control TinyEditor',
            'style':'width:100%',
        }),
        error_messages={'required': 'Please enter a description of the data set'},
        required=True,
    )
    contact_type = forms.ChoiceField(
        label='Type',
        choices=CONTACT_CHOICES,
        required=True,
        help_text='Type of user',
    )
    sql_select = forms.CharField(
        label='Sql Select',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'vLargeTextField',
            'placeholder':'SELECT *'
        }),
        error_messages={'required': 'Please enter the SQL SELECT'},
        required=True,
        help_text='SELECT fields must use alias prefix for example c.id, c.name, c.email',
    )
    sql = forms.CharField(
        label='SQL',
        widget=forms.Textarea(attrs={
            'class':'form-control vLargeTextField',
            'style':'width:100%',
        }),
        error_messages={'required': 'Please enter SQL to generate the data set'},
        required=True,
        help_text='Contact record must be aliased as c, as in FROM whyness_crm_contact AS c or whyness_django_authuser AS c',
    )
    sql_once = forms.BooleanField(
        label='Send only once',
        required=False,
        help_text='Check this box if a message should be sent only once',
    )
    status = forms.ChoiceField(
        label='Status',
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES,
        required=False,
        help_text='Status of this SQL statement',
    )
    class Meta:
        model = UserSQL
        fields = [
            'title', 'description',
            'contact_type',
            'sql_select', 'sql', 'sql_once',
            'status',
        ]

class TrackerDestinationForm(ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=100,
        widget=forms.TextInput(),
        required=False,
        help_text='Title to identify this url',
    )
    url = forms.CharField(
        label='Url',
        max_length=500,
        widget=forms.TextInput(),
        required=True,
        help_text='This is automatically generated from a message',
    )
    status = forms.ChoiceField(
        label='Status',
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES,
        required=False,
        help_text='Status of this url',
    )
    class Meta:
        model = TrackerDestination
        fields = ['title', 'url', 'status',]

