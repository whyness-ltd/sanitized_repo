#----------------------------------------------------------------------
# Whyness crm models
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
import datetime
import logging
import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import Context, Template
from django.utils.text import slugify
from html.parser import HTMLParser

logger = logging.getLogger(__name__)

STATUS_INACTIVE = 0
STATUS_ACTIVE = 1
STATUS_DELETED = 8

STATUS_CHOICES = (
    (STATUS_INACTIVE, ('Inactive')),
    (STATUS_ACTIVE, ('Active')),
)

CONTACT_TBA = 0
CONTACT_PROSPECT = 1
CONTACT_USER = 2

CONTACT_CHOICES = (
    (CONTACT_TBA, ('Please choose')),
    (CONTACT_PROSPECT, ('Prospect')),
    (CONTACT_USER, ('Registered user')),
)

CONTACT_STATUS_PROSPECT = 1

MESSAGE_STATUS_INACTIVE = 0
MESSAGE_STATUS_ACTIVE = 1
MESSAGE_STATUS_CLICKED = 2
MESSAGE_STATUS_DELETED = 8
MESSAGE_STATUS_CHOICES = (
    (MESSAGE_STATUS_INACTIVE, ('Inactive')),
    (MESSAGE_STATUS_ACTIVE, ('Active')),
    (MESSAGE_STATUS_CLICKED, ('Clicked')),
)

UUID_NULL = uuid.UUID('00000000-0000-0000-0000-000000000000')

class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, data):
        self.text += data

class ContactStatus(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="")
    description = models.TextField(default="")
    status = models.SmallIntegerField(default=STATUS_ACTIVE)
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}".format(self.title)
        return ret

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Contact status"

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=150, blank=True)
    xref = models.UUIDField('Contact Reference', default=uuid.uuid4)
    status = models.ForeignKey(
        ContactStatus,
        on_delete=models.CASCADE,
        default=CONTACT_STATUS_PROSPECT,
    )
    is_prospect = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False)
    use_whatsapp = models.BooleanField(default=False)
    use_email = models.BooleanField(default=False)
    update_ip = models.GenericIPAddressField(default='::1')
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    release = models.SmallIntegerField(default=1)

    def __str__(self):
        ret = "{} <{}>".format(self.name, self.email)
        return ret

    def save(self, *args, **kwargs):
        if not self.xref:
            self.xref = uuid.uuid4()
        super(Contact, self).save(*args, **kwargs)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="")
    description = models.TextField(default="")
    slug = models.CharField(max_length=100, unique=True, default="")
    status = models.SmallIntegerField(default=STATUS_ACTIVE)
    is_whatsapp = models.BooleanField(default=False)
    is_email = models.BooleanField(default=False)
    update_ip = models.GenericIPAddressField(default='::1')
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    message_html = models.TextField(blank=True)

    def __str__(self):
        ret = "{}".format(self.title)
        return ret

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Message, self).save(*args, **kwargs)

class AuthUserContactRecord(models.Model):
    id = models.AutoField(primary_key=True)
    contact = models.ForeignKey('whyness_django.AuthUser', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)
    message_status = models.SmallIntegerField(default=MESSAGE_STATUS_ACTIVE)
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}: {}: {}".format(
            self.sent_date,
            self.contact.email,
            self.message.title
        )
        return ret

class ContactRecord(models.Model):
    id = models.AutoField(primary_key=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)
    message_status = models.SmallIntegerField(default=MESSAGE_STATUS_ACTIVE)
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}: {}: {}".format(
            self.sent_date,
            self.contact.email,
            self.message.title
        )
        return ret

class UserSQL(models.Model):
    id = models.AutoField(primary_key=True)
    contact_type = models.SmallIntegerField(default=CONTACT_TBA)
    title = models.CharField(default="", max_length=100)
    description = models.TextField(default="")
    sql_select = models.CharField(max_length=100, default="SELECT *")
    sql = models.TextField(default="")
    status = models.SmallIntegerField(default=STATUS_ACTIVE)
    slug = models.SlugField(max_length=50, unique=True, default="")
    update_ip = models.GenericIPAddressField(default='::1')
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        ret = "{}".format(self.title)
        return ret

class TrackerDestination(models.Model):
    """Tracks destination urls"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(default="", max_length=100)
    url = models.CharField(default="", max_length=500)
    xref = models.UUIDField('Tracker Destination', default=uuid.uuid4)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)
    create_date = models.DateTimeField(auto_now_add=True)

class AuthUserTrackerClick(models.Model):
    """Tracks Registered user destination urls"""
    id = models.AutoField(primary_key=True)
    destination = models.ForeignKey(TrackerDestination, on_delete=models.CASCADE)
    contact = models.ForeignKey('whyness_django.AuthUser', on_delete=models.CASCADE)
    update_ip = models.GenericIPAddressField(default='::1')
    create_date = models.DateTimeField(auto_now_add=True)

class ContactTrackerClick(models.Model):
    """Tracks Contact/prospect destination urls"""
    id = models.AutoField(primary_key=True)
    destination = models.ForeignKey(TrackerDestination, on_delete=models.CASCADE)
    contact = models.ForeignKey('whyness_crm.Contact', on_delete=models.CASCADE)
    update_ip = models.GenericIPAddressField(default='::1')
    create_date = models.DateTimeField(auto_now_add=True)
