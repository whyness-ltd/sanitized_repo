#----------------------------------------------------------------------
# Whyness User feedback models
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

SORT_FIRST = 0
SORT_NORMAL = 1
SORT_LAST = 99
SORT_CHOICES = (
    (SORT_FIRST, ('First')),
    (SORT_NORMAL, ('Normal')),
    (SORT_LAST, ('Last')),
)

class SweetSpotValue(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(default="", max_length=100)
    sort_order = models.SmallIntegerField(default=SORT_NORMAL)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)

    def __str__(self):
        ret = "{}".format(self.title)
        return ret
    class Meta:
        ordering = ['sort_order', 'title']

class SweetSpotStrength(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(default="", max_length=100)
    sort_order = models.SmallIntegerField(default=SORT_NORMAL)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)

    def __str__(self):
        ret = "{}".format(self.title)
        return ret
    class Meta:
        ordering = ['sort_order', 'title']

class SweetSpotImpact(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(default="", max_length=100)
    sort_order = models.SmallIntegerField(default=SORT_NORMAL)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)

    def __str__(self):
        ret = "{}".format(self.title)
        return ret
    class Meta:
        ordering = ['sort_order', 'title']

class SweetSpotConfidence(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(default="", max_length=100)
    sort_order = models.SmallIntegerField(default=SORT_NORMAL)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)

    def __str__(self):
        ret = "{}".format(self.title)
        return ret
    class Meta:
        ordering = ['sort_order', 'title']

class SweetSpot(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        "whyness_django.AuthUser",
        on_delete=models.CASCADE,
        related_name='+',
    )
    ip = models.GenericIPAddressField(default='::1')
    useragent = models.ForeignKey(
        "whyness_django.UserAgent",
        on_delete=models.PROTECT,
        related_name='+',
    )
    value1 = models.ForeignKey(
        SweetSpotValue,
        on_delete=models.CASCADE,
        related_name='+',
    )
    value2 = models.ForeignKey(
        SweetSpotValue,
        on_delete=models.CASCADE,
        related_name='+',
    )
    value3 = models.ForeignKey(
        SweetSpotValue,
        on_delete=models.CASCADE,
        related_name='+',
    )
    valueother = models.CharField(default="", blank=True, max_length=100)
    valueconfidence = models.ForeignKey(
        SweetSpotConfidence,
        on_delete=models.CASCADE,
        related_name='+',
    )
    strength1 = models.ForeignKey(
        SweetSpotStrength,
        on_delete=models.CASCADE,
        related_name='+',
    )
    strength2 = models.ForeignKey(
        SweetSpotStrength,
        on_delete=models.CASCADE,
        related_name='+',
    )
    strength3 = models.ForeignKey(
        SweetSpotStrength,
        on_delete=models.CASCADE,
        related_name='+',
    )
    strengthother = models.CharField(default="", blank=True, max_length=100)
    strengthconfidence = models.ForeignKey(
        SweetSpotConfidence,
        on_delete=models.CASCADE,
        related_name='+',
    )
    impact1 = models.ForeignKey(
        SweetSpotImpact,
        on_delete=models.CASCADE,
        related_name='+',
    )
    impact2 = models.ForeignKey(
        SweetSpotImpact,
        on_delete=models.CASCADE,
        related_name='+',
    )
    impact3 = models.ForeignKey(
        SweetSpotImpact,
        on_delete=models.CASCADE,
        related_name='+',
    )
    impactother = models.CharField(default="", blank=True, max_length=100)
    impactconfidence = models.ForeignKey(
        SweetSpotConfidence,
        on_delete=models.CASCADE,
        related_name='+',
    )
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}:{}:{}".format(self.id, self.create_date, self.user)
        return ret

    class Meta:
        ordering = ['-id']

