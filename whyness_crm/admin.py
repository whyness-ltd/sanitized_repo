#----------------------------------------------------------------------
# Whyness crm admin
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
import logging

from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html

from whyness_crm.models import Contact
from whyness_crm.models import ContactRecord
from whyness_crm.models import ContactStatus
from whyness_crm.models import Message
from whyness_crm.models import UserSQL
from whyness_crm.models import TrackerDestination

from whyness_crm.forms import ContactForm
from whyness_crm.forms import MessageForm
from whyness_crm.forms import TrackerDestinationForm
from whyness_crm.forms import UserSQLForm

from whyness_crm.models import STATUS_ACTIVE
from whyness_crm.models import STATUS_INACTIVE
from whyness_crm.views import dashboard

from whyness_django.models import AuthUser

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
class ContactRecordInline(admin.TabularInline):
    model = ContactRecord
    fk_name = 'contact'
    extra = 0
    readonly_fields = [
        'message', 'status', 'message_status',
    ]

class ContactAdmin(admin.ModelAdmin):
    form = ContactForm
    fields = (
        'id', 'name', 'email',
        'release',
        'status', 'is_prospect', 'is_registered',
        'use_email',
        ('update_date', 'create_date'),
    )

    inlines = [ContactRecordInline,]
    readonly_fields = [
        'id',
        'update_date', 'create_date']
    search_fields = ['name']
    list_display = [
        'name',
        'email',
        'release',
        is_active,
    ]
    ordering = ['name']

class ContactStatusAdmin(admin.ModelAdmin):
    Model = ContactStatus
    fields = (
        'title',
        'description',
        'status',
        ('update_date', 'create_date'),
    )

class MessageAdmin(admin.ModelAdmin):
    form = MessageForm
    fields = (
        'title',
        'description',
        'from_user',
        'message_html',
        'is_email',
        'status',
        ('update_date', 'create_date'),
    )

    readonly_fields = [
        'update_date', 'create_date'
    ]
    search_fields = ['title']
    list_display = [
        'title',
        'from_user',
        'is_whatsapp',
        'is_email',
        is_active,
    ]
    ordering = ['-status', 'title']

class TrackerDestinationAdmin(admin.ModelAdmin):
    form = TrackerDestinationForm
    fields = (
        'title', 'url',
        'status',
        'create_date',
    )
    readonly_fields = ['url', 'create_date']
    search_fields = ['title']
    list_display = [
        'create_date',
        'title',
        is_active,
    ]
    ordering = ['title']

class UserSQLAdmin(admin.ModelAdmin):
    form = UserSQLForm
    fields = (
        'title', 'description',
        'contact_type',
        'sql_select', 'sql',
        'slug', 'status', 'update_user',
        ('update_date', 'create_date'),
    )
    readonly_fields = ['update_user', 'update_date', 'create_date']
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title']
    list_display = [
        'title',
        is_active,
    ]
    ordering = ['status', 'title']

    def save_model(self, request, obj, form, change):
            obj.update_user = request.user
            super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactStatus, ContactStatusAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserSQL, UserSQLAdmin)
admin.site.register(TrackerDestination, TrackerDestinationAdmin)
