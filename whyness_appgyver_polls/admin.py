#----------------------------------------------------------------------
# Whyness Dream Job admin
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
import logging
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html

from whyness_appgyver_polls.forms import SweetSpotValueForm
from whyness_appgyver_polls.forms import SweetSpotStrengthForm
from whyness_appgyver_polls.forms import SweetSpotImpactForm

from whyness_appgyver_polls.models import DreamJob
from whyness_appgyver_polls.models import SweetSpotValue
from whyness_appgyver_polls.models import SweetSpotStrength
from whyness_appgyver_polls.models import SweetSpotImpact
from whyness_appgyver_polls.models import SweetSpot
from whyness_appgyver_polls.models import STATUS_ACTIVE
from whyness_appgyver_polls.models import STATUS_INACTIVE

logger = logging.getLogger(__name__)

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

class DreamJobAdmin(admin.ModelAdmin):
    model = DreamJob
    fields = [
		'user', 'ip', 'useragent',
		'role1', 'role2', 'role3',
		'roleother', 'roleconfidence',
		'profession1', 'profession2', 'profession3',
		'professionother', 'professionconfidence',
		'company_size', 'office_culture',
		'create_date',
	]
    readonly_fields = [
		'user', 'ip', 'useragent',
		'role1', 'role2', 'role3',
		'roleother', 'roleconfidence',
		'profession1', 'profession2', 'profession3',
		'professionother', 'professionconfidence',
		'company_size', 'office_culture',
		'create_date'
	]
    ordering = ['-id']

class SweetSpotValueAdmin(admin.ModelAdmin):
    form = SweetSpotValueForm
    fields = ['id', 'title', 'status']
    readonly_fields = ['id', ]
    ordering = ['title']
    list_display = ('title', is_active)

class SweetSpotStrengthAdmin(admin.ModelAdmin):
    form = SweetSpotStrengthForm
    fields = ['id', 'title', 'status']
    readonly_fields = ['id', ]
    ordering = ['title']
    list_display = ('title', is_active)

class SweetSpotImpactAdmin(admin.ModelAdmin):
    form = SweetSpotImpactForm
    fields = ['id', 'title', 'status']
    readonly_fields = ['id', ]
    ordering = ['title']
    list_display = ('title', is_active)

class SweetSpotAdmin(admin.ModelAdmin):
    model = SweetSpot
    fields = [
        'user', 'ip', 'useragent',
        'value1', 'value2', 'value3',
        'valueother', 'valueconfidence',
		'strength1', 'strength2', 'strength3',
		'strengthother', 'strengthconfidence',
        'impact1', 'impact2', 'impact3',
        'impactother', 'impactconfidence',
		'create_date',
	]
    readonly_fields = [
		'user', 'ip', 'useragent',
        'value1', 'value2', 'value3',
        'valueother', 'valueconfidence',
		'strength1', 'strength2', 'strength3',
		'strengthother', 'strengthconfidence',
        'impact1', 'impact2', 'impact3',
        'impactother', 'impactconfidence',
		'create_date'
	]
    ordering = ['-id']

admin.site.register(DreamJob, DreamJobAdmin)
admin.site.register(SweetSpotValue, SweetSpotValueAdmin)
admin.site.register(SweetSpotStrength, SweetSpotStrengthAdmin)
admin.site.register(SweetSpotImpact, SweetSpotImpactAdmin)
admin.site.register(SweetSpot, SweetSpotAdmin)
