from django import forms
from django.forms import ModelForm

from whyness_appgyver_polls.models import SweetSpotValue
from whyness_appgyver_polls.models import SweetSpotStrength
from whyness_appgyver_polls.models import SweetSpotImpact
from whyness_appgyver_polls.models import STATUS_ACTIVE
from whyness_appgyver_polls.models import STATUS_INACTIVE
from whyness_appgyver_polls.models import STATUS_CHOICES

class SweetSpotValueForm(ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control vTextField',
            'placeholder':'Title',
        }),
        error_messages={'required': 'Please enter a title'},
        help_text='This is a sweet spot value',
    )
    status = forms.ChoiceField(
        label='Status',
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES,
        required=False,
        help_text='Status',
    )
    class Meta:
        model = SweetSpotValue
        fields = ['title', 'status']

class SweetSpotStrengthForm(ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control vTextField',
            'placeholder':'Title',
        }),
        error_messages={'required': 'Please enter a title'},
        help_text='This is a sweet spot strength',
    )
    status = forms.ChoiceField(
        label='Status',
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES,
        required=False,
        help_text='Status',
    )
    class Meta:
        model = SweetSpotStrength
        fields = ['title', 'status']


class SweetSpotImpactForm(ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control vTextField',
            'placeholder':'Title',
        }),
        error_messages={'required': 'Please enter a title'},
        help_text='This is a sweet spot impact',
    )
    status = forms.ChoiceField(
        label='Status',
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES,
        required=False,
        help_text='Status',
    )
    class Meta:
        model = SweetSpotImpact
        fields = ['title', 'status']



