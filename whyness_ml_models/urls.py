#----------------------------------------------------------------------
# Whyness ml models urls
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework import routers
from . import views

app_name="whyness_ml_models"
urlpatterns = [
    path(
        'v1/ml/mbti/',
        views.ApiMBTI.as_view(),
        name='ml-mbti'
    ),
]
