#----------------------------------------------------------------------
# Whyness AppGyver poll urls
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework import routers
from . import views

urlpatterns = [
    path(
        'v1/agpoll/sweetspotvalues/',
        views.ApiSweetSpotValue.as_view(),
        name='agpoll-sweetspotvalues'
    ),
    path(
        'v1/agpoll/sweetspotstrengths/',
        views.ApiSweetSpotStrength.as_view(),
        name='agpoll-sweetspotstrengths'
    ),
    path(
        'v1/agpoll/sweetspotimpacts/',
        views.ApiSweetSpotImpact.as_view(),
        name='agpoll-sweetspotimpacts'
    ),
    path(
        'v1/agpoll/sweetspot/<int:id>/',
        views.ApiSweetSpot.as_view(),
        name='agpoll-sweetspot'
    ),
    path(
        'v1/agpoll/sweetspot/',
        views.ApiSweetSpot.as_view(),
        name='agpoll-sweetspot'
    ),

    path(
        'v1/agpoll/dreamjob/',
        views.ApiDreamJob.as_view(),
        name='agpoll-dreamjob'
    ),
    path(
        'v1/agpoll/dreamjob/<str:id>/',
        views.ApiDreamJob.as_view(),
        name='agpoll-dreamjob'
    ),
]
