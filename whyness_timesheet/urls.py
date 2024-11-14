#----------------------------------------------------------------------
# Whyness timesheet urls
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from django.contrib import admin
from django.urls import path, include
from whyness_timesheet import views

urlpatterns = [
    path('timesheets/', views.timesheets, name='timesheets'),
    path('timesheets-csv/', views.timesheet_csv, name='timesheets-csv'),
    path('timesheets-detail-csv/', views.timesheet_detail_csv, name='timesheets-detail-csv'),
]
