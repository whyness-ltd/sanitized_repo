#----------------------------------------------------------------------
# Whyness admin
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

"""
"""

import logging

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
from whyness_django.models import STATUS_ACTIVE
from whyness_django.models import STATUS_INACTIVE

from whyness_django.forms import AudioForm
from whyness_django.forms import QuestionForm

from whyness_django.models import TRANSCRIPT_STATUS_INACTIVE
from whyness_django.models import TRANSCRIPT_STATUS_ACTIVE
from whyness_django.models import TRANSCRIPT_STATUS_SENT_FOR_TRANSCRIPTION
from whyness_django.models import TRANSCRIPT_STATUS_IN_PROGRESS
from whyness_django.models import TRANSCRIPT_STATUS_TRANSCRIBED
from whyness_django.models import TRANSCRIPT_STATUS_TRANSCRIBE_FAILED
from whyness_django.models import TRANSCRIPT_STATUS_REPRESENTATIONAL_SYSTEM
from whyness_django.models import TRANSCRIPT_STATUS_MBTI
from whyness_django.models import TRANSCRIPT_STATUS_NEEDS_CONVERTING
from whyness_django.models import TRANSCRIPT_STATUS_DELETED
from whyness_django.models import TRANSCRIPT_STATUS_ERROR

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

# Admin classes
class AuthUserAdmin(admin.ModelAdmin):
    form = AudioForm
    fields = (
        'uid',
        'name',
        'email',
        'status',
        ('update_date', 'create_date'),
    )

    readonly_fields = [
        'uid',
        'name',
        'email',
        'status',
        'update_date', 'create_date']
    search_fields = ['name']
    list_display = [
        'id',
        'name',
        'email',
        is_active,
    ]
    ordering = ['name']

class AudioAdmin(admin.ModelAdmin):
    form = AudioForm
    fields = (
        'user',
        'question',
        'status',
        'representational_system',
        'transcribe_job_name',
        'transcript', 'transcript_s3',
        'transcript_json',
        'transcribe_status',
        'transcribe_status_json',
        ('update_date', 'create_date'),
    )

    readonly_fields = [
        'user',
        'question',
        'status',
        'representational_system',
        'transcribe_job_name',
        'transcript', 'transcript_s3',
        'transcribe_status',
        'transcribe_status_json',
        'transcript_json',
        'update_date', 'create_date']
    search_fields = ['title']
    actions = ['transcribe_audio']
    list_display = [
        'id',
        'status',
        'user',
        'update_date',
    ]

    @admin.action(description='Transcribe audio')
    def transcribe_audio(self, request, queryset):
        for m in queryset:
            logger.debug(m)
            if id and m.status == TRANSCRIPT_STATUS_ACTIVE:
                msg = '{}: Transcribe'.format(m.status)
                logger.debug(msg)
                m.transcribe()
            if id and m.status == TRANSCRIPT_STATUS_SENT_FOR_TRANSCRIPTION:
                msg = '{}: Transcribe sent'.format(m.status)
                logger.debug(msg)
                m.transcribe_status_check()
            if id and m.status == TRANSCRIPT_STATUS_NEEDS_CONVERTING:
                msg = '{}: Transcribe convert'.format(m.status)
                logger.debug(msg)
                m.convert_for_transcription()
            if id and m.status == TRANSCRIPT_STATUS_TRANSCRIBED:
                msg = '{}: Represent'.format(m.status)
                logger.debug(msg)
                m.get_representational_system()
            if id and m.status == TRANSCRIPT_STATUS_REPRESENTATIONAL_SYSTEM:
                msg = '{}: MBTI'.format(m.status)
                logger.debug(msg)
                m.process_mbti()
        msg = "Audio file(s) sent for transcription"
        self.message_user(request, msg, messages.SUCCESS)

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    fields = ('question', 'sort_order', 'status',
        ('update_date', 'update_user', 'create_date'),
    )
    readonly_fields = ['update_user', 'update_date', 'create_date']
    list_display = ['question', 'id', is_active]

    def save_model(self, request, obj, form, change):
            obj.update_user = request.user
            super().save_model(request, obj, form, change)

class RoleTypeAttributesInline(admin.TabularInline):
    model = Role.attributes.through
    extra = 2

class TypeAttributesAdmin(admin.ModelAdmin):
    model = TypeAttributes
    fields = ('title', 'description')

class ProfessionAdmin(admin.ModelAdmin):
    model = Profession
    fields = ('title',)

class RoleAdmin(admin.ModelAdmin):
    model = Role
    #fields = ('profession', 'title',)
    inlines = [
        RoleTypeAttributesInline,
    ]
    exclude = ['attributes',]
    list_display = [
        'title',
        'profession',
    ]
    list_filter = ['profession', ]
    ordering = ['title']
    search_fields = ['title']

class TrackerItemAdmin(admin.ModelAdmin):
    model = TrackerItem
    fields = ('title', 'description')
    readonly_fields = ['title']
    ordering = ['title']

class TrackerLogAdmin(admin.ModelAdmin):
    model = TrackerLog
    fields = ['user', 'item', 'ip', 'useragent', 'method', 'create_date']
    readonly_fields = ['user', 'item', 'ip', 'useragent', 'method', 'create_date']
    ordering = ['-id']

class UserAgentAdmin(admin.ModelAdmin):
    model = UserAgent
    fields = ('useragent',)
    readonly_fields = ['useragent']
    ordering = ['useragent']

# Register your models here.
admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TypeAttributes, TypeAttributesAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(TrackerLog, TrackerLogAdmin)
admin.site.register(TrackerItem, TrackerItemAdmin)
admin.site.register(UserAgent, UserAgentAdmin)

