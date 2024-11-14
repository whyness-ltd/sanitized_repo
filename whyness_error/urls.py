#----------------------------------------------------------------------
# Whyness errorlog api urls
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from django.contrib import admin
from django.urls import path, include
from whyness_error import views

app_name="whyness_error"
urlpatterns = [
    path('v1/error/log/', views.ApiErrorLog.as_view(), name='api-error-log'),
]



