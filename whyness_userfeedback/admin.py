#----------------------------------------------------------------------
# Whyness User feedback admin
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html

from whyness_django.models import Audio
from whyness_django.models import AuthUser
from whyness_django.models import Question
from whyness_django.models import TypeAttributes
from whyness_django.models import Profession
from whyness_django.models import Role
from whyness_django.models import TrackerLog, TrackerItem, UserAgent

from whyness_userfeedback.models import SweetSpotValue
from whyness_userfeedback.models import SweetSpotStrength
from whyness_userfeedback.models import SweetSpotImpact
from whyness_userfeedback.models import SweetSpotConfidence
from whyness_userfeedback.models import SweetSpot

from whyness_userfeedback.models import STATUS_ACTIVE
from whyness_userfeedback.models import STATUS_INACTIVE

from whyness_userfeedback.forms import SweetSpotValueForm
from whyness_userfeedback.forms import SweetSpotStrengthForm
from whyness_userfeedback.forms import SweetSpotImpactForm
from whyness_userfeedback.forms import SweetSpotConfidenceForm

def is_active(obj):
    """Function to display tick cross icon for status"""
    icon = '✔'
    src = None
    if obj.status == STATUS_ACTIVE:
        alt = 'Active'
        msg = '✔'
    elif obj.status == STATUS_INACTIVE:
        alt = 'Inactive'
        msg = '✕'
    else:
        alt = 'Unknown'
        msg = '?'
    return format_html('<span title="{}">{}</span>'.format(alt, msg))
is_active.short_description = 'Active'

class SweetSpotValueAdmin(admin.ModelAdmin):
    form = SweetSpotValueForm
    fields = (
        'title',
        'sort_order',
        'status',
    )
    search_fields = ['title']
    list_display = [
        'title',
        is_active,
    ]
    ordering = ['sort_order', 'title']
class SweetSpotStrengthAdmin(admin.ModelAdmin):
    form = SweetSpotStrengthForm
    fields = (
        'title',
        'sort_order',
        'status',
    )
    search_fields = ['title']
    list_display = [
        'title',
        is_active,
    ]
    ordering = ['sort_order', 'title']
class SweetSpotImpactAdmin(admin.ModelAdmin):
    form = SweetSpotImpactForm
    fields = (
        'title',
        'sort_order',
        'status',
    )
    search_fields = ['title']
    list_display = [
        'title',
        is_active,
    ]
    ordering = ['sort_order', 'title']
class SweetSpotConfidenceAdmin(admin.ModelAdmin):
    form = SweetSpotConfidenceForm
    fields = (
        'title',
        'sort_order',
        'status',
    )
    search_fields = ['title']
    list_display = [
        'title',
        is_active,
    ]
    ordering = ['sort_order', 'title']
class SweetSpotAdmin(admin.ModelAdmin):
    form = SweetSpotConfidenceForm
    fields = (
        'user',
        'ip',
        'useragent',
        'value1',
        'value2',
        'value3',
        'valueother',
        'valueconfidence',
        'strength1',
        'strength2',
        'strength3',
        'strengthother',
        'strengthconfidence',
        'impact1',
        'impact2',
        'impact3',
        'impactother',
        'impactconfidence',
        ('update_date', 'create_date'),
    )
    search_fields = ['user']
    list_display = [
        'user',
        'value1',
        'strength1',
        'impact1',
        'create_date',
    ]
    readonly_fields = [
        'user',
        'ip',
        'useragent',
        'value1',
        'value2',
        'value3',
        'valueother',
        'valueconfidence',
        'strength1',
        'strength2',
        'strength3',
        'strengthother',
        'strengthconfidence',
        'impact1',
        'impact2',
        'impact3',
        'impactother',
        'impactconfidence',
        'update_date',
        'create_date',
    ]

# Register your models here.
admin.site.register(SweetSpotValue, SweetSpotValueAdmin)
admin.site.register(SweetSpotStrength, SweetSpotStrengthAdmin)
admin.site.register(SweetSpotImpact, SweetSpotImpactAdmin)
admin.site.register(SweetSpotConfidence, SweetSpotConfidenceAdmin)
admin.site.register(SweetSpot, SweetSpotAdmin)
