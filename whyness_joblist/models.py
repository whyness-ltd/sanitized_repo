#----------------------------------------------------------------------
# Whyness job list models
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
from django.db import models

from whyness_django.models import AuthUser

STATUS_INACTIVE = 0
STATUS_ACTIVE = 1
STATUS_DELETED = 8

STATUS_CHOICES = (
    (STATUS_INACTIVE, ('Inactive')),
    (STATUS_ACTIVE, ('Active')),
)

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=2)
    code3 = models.CharField(max_length=3)
    update_ip = models.GenericIPAddressField(default='::1')
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Industry(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    update_ip = models.GenericIPAddressField(default='::1')
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="", blank=True)
    logo = models.CharField(max_length=100, default="", blank=True)
    overview = models.TextField(default="", blank=True)
    industry = models.CharField(max_length=100, default="", blank=True)
    size = models.CharField(max_length=100, default="", blank=True)
    website = models.URLField(default="", blank=True)
    email = models.EmailField(max_length=150, default="", blank=True)
    values1 = models.CharField(max_length=100, default="", blank=True)
    values2 = models.CharField(max_length=100, default="", blank=True)
    values3 = models.CharField(max_length=100, default="", blank=True)
    values4 = models.CharField(max_length=100, default="", blank=True)
    values5 = models.CharField(max_length=100, default="", blank=True)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)
    update_ip = models.GenericIPAddressField(default='::1')
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"

class Job(models.Model):
    id = models.AutoField(primary_key=True)
    job_id = models.CharField(max_length=100, default="", blank=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    title = models.CharField(max_length=100, default="", blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT)
    location = models.CharField(max_length=100, default="", blank=True)
    job_type = models.CharField(max_length=100, default="", blank=True)
    usp = models.TextField(default="", blank=True)
    ssvalues1 = models.CharField(max_length=100, default="", blank=True)
    ssvalues2 = models.CharField(max_length=100, default="", blank=True)
    ssvalues3 = models.CharField(max_length=100, default="", blank=True)
    ssvalues4 = models.CharField(max_length=100, default="", blank=True)
    ssvalues5 = models.CharField(max_length=100, default="", blank=True)
    strength1 = models.CharField(max_length=100, default="", blank=True)
    strength2 = models.CharField(max_length=100, default="", blank=True)
    strength3 = models.CharField(max_length=100, default="", blank=True)
    strength4 = models.CharField(max_length=100, default="", blank=True)
    strength5 = models.CharField(max_length=100, default="", blank=True)
    impact1 = models.CharField(max_length=100, default="", blank=True)
    impact2 = models.CharField(max_length=100, default="", blank=True)
    impact3 = models.CharField(max_length=100, default="", blank=True)
    skills = models.TextField(default="", blank=True)
    development = models.TextField(default="", blank=True)
    culture = models.TextField(default="", blank=True)
    edi_score = models.CharField(max_length=100, default="", blank=True)
    glassdoor_rating = models.CharField(max_length=100, default="", blank=True)
    job_link = models.URLField(default="", blank=True)
    eligibility = models.TextField(default="", blank=True)
    status = models.SmallIntegerField(default=STATUS_ACTIVE)
    update_ip = models.GenericIPAddressField(default='::1')
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True)

    def __str__(self):
        ret = "{}: {} - {}".format(self.job_id, self.company, self.title)
        return ret

class JobList(models.Model):
    """Model to represent a job view, it's created in sql rather than a view"""
    id = models.AutoField(primary_key=True)
    job_id = models.CharField(max_length=100, default="")
    job_ref = models.CharField(max_length=100, default="")
    company_id = models.IntegerField(default=0)
    company = models.CharField(max_length=100, default="")
    company_website = models.CharField(max_length=250, default="")
    logo = models.CharField(max_length=100, default="")
    title = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=100, default="")
    location = models.CharField(max_length=100, default="")
    job_type = models.CharField(max_length=100, default="")
    job_link = models.URLField(default="")
    status = models.CharField(max_length=100, default="")

    class Meta:
        managed = False

class JobShow(models.Model):
    """Model to show a job, it's created in sql rather than a view"""
    id = models.AutoField(primary_key=True)
    job_id = models.CharField(max_length=100, default="")
    job_ref = models.CharField(max_length=100, default="")
    company = models.CharField(max_length=100, default="")
    company_website = models.URLField(default="")
    logo = models.CharField(max_length=100, default="")
    title = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=100, default="")
    industry = models.CharField(max_length=100, default="")
    location = models.CharField(max_length=100, default="")
    job_type = models.CharField(max_length=100, default="")
    usp = models.CharField(max_length=100, default="")
    values1 = models.CharField(max_length=100, default="")
    values2 = models.CharField(max_length=100, default="")
    values3 = models.CharField(max_length=100, default="")
    values4 = models.CharField(max_length=100, default="")
    values5 = models.CharField(max_length=100, default="")
    ssvalues1 = models.CharField(max_length=100, default="")
    ssvalues2 = models.CharField(max_length=100, default="")
    ssvalues3 = models.CharField(max_length=100, default="")
    ssvalues4 = models.CharField(max_length=100, default="")
    ssvalues5 = models.CharField(max_length=100, default="")
    strength1 = models.CharField(max_length=100, default="")
    strength2 = models.CharField(max_length=100, default="")
    strength3 = models.CharField(max_length=100, default="")
    strength4 = models.CharField(max_length=100, default="")
    strength5 = models.CharField(max_length=100, default="")
    impact1 = models.CharField(max_length=100, default="")
    impact2 = models.CharField(max_length=100, default="")
    impact3 = models.CharField(max_length=100, default="")
    skills = models.TextField(default="", blank=True)
    development = models.CharField(max_length=100, default="")
    culture = models.CharField(max_length=100, default="")
    edi_score = models.CharField(max_length=100, default="")
    glassdoor_rating = models.CharField(max_length=100, default="")
    job_link = models.CharField(max_length=100, default="")
    eligibility = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=100, default="")
    create_date = models.CharField(max_length=100, default="")

    class Meta:
        managed = False

class JobStatus(models.Model):
    """Records user/job status"""
    class JobState(models.IntegerChoices):
        UNSEEN = 0
        SEEN = 1
        LIKED = 2
        REJECTED = 3
        APPLIED = 4

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.PROTECT,
    )
    job = models.ForeignKey(Job, on_delete=models.PROTECT)
    update_ip = models.GenericIPAddressField(default='::1')
    status = models.IntegerField(choices=JobState.choices, default=JobState.UNSEEN)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}: {}".format(self.create_date, self.status.label)
        return ret
