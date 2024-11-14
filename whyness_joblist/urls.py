#----------------------------------------------------------------------
# Whyness job list urls
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from django.contrib import admin
from django.urls import path, include
from whyness_joblist import views

app_name="whyness_joblist"
urlpatterns = [
    path(
        'v1/joblist/',
        views.ApiList.as_view(),
        name='joblist-list'
    ),
    path(
        'v1/joblist/<int:id>/',
        views.ApiJob.as_view(),
        name='joblist-job'
    ),
    path(
        'v1/joblist/<str:filter>/',
        views.ApiList.as_view(),
        name='joblist-jobstatus'
    ),
]

