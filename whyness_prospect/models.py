#----------------------------------------------------------------------
# Whyness prospects models
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
from django.db import models

import logging
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

STATUS_INACTIVE = 0
STATUS_ACTIVE = 1
STATUS_DELETED = 8

STATUS_CHOICES = (
    (STATUS_INACTIVE, ('Inactive')),
    (STATUS_ACTIVE, ('Active')),
)

class Prospect(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=150, blank=True)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)
    update_ip = models.GenericIPAddressField(default='::1')
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        ret = "{} <{}>".format(self.name, self.email)
        return ret

    def save(self, *args, **kwargs):
        if not self.update_user_id:
            self.update_user_id = 1
        super(Prospect, self).save(*args, **kwargs)
