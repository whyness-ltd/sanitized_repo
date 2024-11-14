#----------------------------------------------------------------------
# Whyness AppGyver poll models
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from django.db import models
from django.conf import settings

STATUS_INACTIVE = 0
STATUS_ACTIVE = 1
STATUS_DELETED = 8

STATUS_CHOICES = (
    (STATUS_INACTIVE, ('Inactive')),
    (STATUS_ACTIVE, ('Active')),
)

class DreamJob(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("whyness_django.AuthUser", on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(default='::1')
    useragent = models.ForeignKey("whyness_django.UserAgent", on_delete=models.PROTECT)
    role1 = models.CharField(default="", max_length=100)
    role2 = models.CharField(default="", max_length=100)
    role3 = models.CharField(default="", max_length=100)
    roleother = models.CharField(default="", max_length=100)
    roleconfidence = models.CharField(default="", max_length=100)
    profession1 = models.CharField(default="", max_length=100)
    profession2 = models.CharField(default="", max_length=100)
    profession3 = models.CharField(default="", max_length=100)
    professionother = models.CharField(default="", max_length=100)
    professionconfidence = models.CharField(default="", max_length=100)
    company_size = models.CharField(default="", max_length=100)
    office_culture = models.CharField(default="", max_length=100)
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}:{}:{}".format(self.id, self.create_date, self.user)
        return ret

    class Meta:
        ordering = ['-id']

class SweetSpotValue(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(default="", max_length=100)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)

    def __str__(self):
        ret = "{}".format(self.title)
        return ret

class SweetSpotStrength(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(default="", max_length=100)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)

    def __str__(self):
        ret = "{}".format(self.title)
        return ret

class SweetSpotImpact(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(default="", max_length=100)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)

    def __str__(self):
        ret = "{}".format(self.title)
        return ret

class SweetSpot(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("whyness_django.AuthUser", on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(default='::1')
    useragent = models.ForeignKey("whyness_django.UserAgent", on_delete=models.PROTECT)
    value1 = models.CharField(default="", max_length=100)
    value2 = models.CharField(default="", max_length=100)
    value3 = models.CharField(default="", max_length=100)
    valueother = models.CharField(default="", max_length=100)
    valueconfidence = models.CharField(default="", max_length=100)
    strength1 = models.CharField(default="", max_length=100)
    strength2 = models.CharField(default="", max_length=100)
    strength3 = models.CharField(default="", max_length=100)
    strengthother = models.CharField(default="", max_length=100)
    strengthconfidence = models.CharField(default="", max_length=100)
    impact1 = models.CharField(default="", max_length=100)
    impact2 = models.CharField(default="", max_length=100)
    impact3 = models.CharField(default="", max_length=100)
    impactother = models.CharField(default="", max_length=100)
    impactconfidence = models.CharField(default="", max_length=100)
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}:{}:{}".format(self.id, self.create_date, self.user)
        return ret

    class Meta:
        ordering = ['-id']

