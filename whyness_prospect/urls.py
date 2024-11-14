#----------------------------------------------------------------------
# Whyness prospect urls
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from django.contrib import admin
from django.urls import path, include
from whyness_prospect import views

urlpatterns = [
    path('prospect/', views.prospect_index, name='prospect_index'),
    path('prospect/<int:id>/', views.prospect, name='prospect'),
    path('api/v1/prospect/<int:id>/', views.ApiProspect.as_view(), name='api-prospect'),
    path('api/v1/prospect/<str:email>/', views.ApiProspect.as_view(), name='api-prospect'),
    path('api/v1/prospect/', views.ApiProspect.as_view(), name='api-prospect'),
]

