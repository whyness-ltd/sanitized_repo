#----------------------------------------------------------------------
# Whyness crm urls
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from django.contrib import admin
from django.urls import path, include
from whyness_crowdsource import views

app_name="whyness_crowdsource"
urlpatterns = [
    # Stories
    path(
        'v1/crowdsource/story/grant/',
        views.ApiStoryGrant.as_view(),
        name='story-grant'
    ),
    path(
        'v1/crowdsource/story/reviews/',
        views.ApiStoryReviews.as_view(),
        name='story-review'
    ),
    path(
        'v1/crowdsource/story/status/',
        views.ApiStoryStatus.as_view(),
        name='story-status'
    ),
    path(
        'v1/crowdsource/story/stories/',
        views.ApiStoryStories.as_view(),
        name='story-stories'
    ),
    path(
        'v1/crowdsource/story/start/',
        views.ApiStoryStart.as_view(),
        name='story-start'
    ),
    # Reviews
    path(
        'v1/crowdsource/review/status/',
        views.ApiReviewStatus.as_view(),
        name='review'
    ),
    path(
        'v1/crowdsource/review/start/',
        views.ApiReviewStart.as_view(),
        name='review-start'
    ),
    path(
        'v1/crowdsource/review/stories/',
        views.ApiReviewStories.as_view(),
        name='review-stories'
    ),
    path(
        'v1/crowdsource/review/reject/',
        views.ApiReviewReject.as_view(),
        name='review-reject'
    ),
    path(
        'v1/crowdsource/review/close/',
        views.ApiReviewClose.as_view(),
        name='review-close'
    ),
]
