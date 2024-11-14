#----------------------------------------------------------------------
# Whyness user feedback api urls
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from django.contrib import admin
from django.urls import path, include
from whyness_userfeedback_api import views

app_name="whyness_userfeedback_api"
urlpatterns = [
    path('v1/user/feedback/', views.ApiUserFeedback.as_view(), name='api-user-feedback'),
]


