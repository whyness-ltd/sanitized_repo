#----------------------------------------------------------------------
# Whyness crowdsource models
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
import logging

from django.db import models
from django.conf import settings

from whyness_django.models import AuthUser

from whyness_userfeedback.models import SweetSpotValue
from whyness_userfeedback.models import SweetSpotStrength
from whyness_userfeedback.models import SweetSpotImpact
from whyness_userfeedback.models import SweetSpotConfidence

logger = logging.getLogger(__name__)

STATUS_INACTIVE = 0
STATUS_ACTIVE = 1
STATUS_DELETED = 8

STATUS_CHOICES = (
    (STATUS_INACTIVE, ('Inactive')),
    (STATUS_ACTIVE, ('Active')),
)

STORIES_INACTIVE = 0
STORIES_AVAILABLE = 5
STORIES_NOT_ENOUGH = 10
STORIES_NOT_GRANTED = 15
STORIES_WAITING_FOR_REVIEW = 20
STORIES_IN_PROGRESS = 25
STORIES_REJECTED = 30
STORIES_DELETED = 99

STORIES_CHOICES = (
    (STORIES_AVAILABLE, ('Enough stories ready for review')),
    (STORIES_NOT_ENOUGH, ('Not enough stories')),
    (STORIES_NOT_GRANTED, ('Permission not granted')),
    (STORIES_WAITING_FOR_REVIEW, ('Waiting for a reviewer')),
    (STORIES_IN_PROGRESS, ('With a reviewer')),
    (STORIES_REJECTED, ('Returned by the reviewer')),
)

REVIEW_INACTIVE = 0
REVIEW_OPEN = 5
REVIEW_COMPLETED = 10
REVIEW_REJECTED = 15
REVIEW_DELETED = 99

REVIEW_CHOICES = (
    (REVIEW_INACTIVE, ('-')),
    (REVIEW_OPEN, ('Open')),
    (REVIEW_COMPLETED, ('Completed')),
    (REVIEW_REJECTED, ('Rejected')),
    (REVIEW_DELETED, ('Deleted')),
)

class StoryGrant(models.Model):
    """Stores grant status used to allow crowdsourcing"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.PROTECT,
    )
    update_ip = models.GenericIPAddressField(default='::1')
    is_granted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}: {}".format(self.create_date, self.is_granted)
        return ret

class Review(models.Model):
    """Review control"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.PROTECT,
        related_name='+',
    )
    status = models.SmallIntegerField(default=REVIEW_INACTIVE)
    updated_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}: {}".format(self.updated_date, self.status)
        return ret

class ReviewReviewer(models.Model):
    """Reviewer revieweing a set of stories"""
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.PROTECT,
        related_name='+',
    )
    reviewer = models.ForeignKey(
        AuthUser,
        on_delete=models.PROTECT,
        related_name='+',
    )
    feedback = models.TextField(default="")
    status = models.SmallIntegerField(default=REVIEW_INACTIVE)
    updated_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}: {}".format(self.updated_date, self.status)
        return ret

class ReviewStories(models.Model):
    """Stories for Review"""
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    story = models.ForeignKey('whyness_django.Audio', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}".format(self.create_date)
        return ret

class ReviewFeedback(models.Model):
    """Feedback on a Review"""
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    feedback = models.TextField(default="")
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = "{}".format(self.create_date)
        return ret

class ReviewSweetSpot(models.Model):
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
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
        ret = "{}".format(self.create_date)
        return ret

    class Meta:
        ordering = ['-id']

