#----------------------------------------------------------------------
# Whyness crm urls
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from django.contrib import admin
from django.urls import path, include
from whyness_crm import views

app_name="whyness_crm"
urlpatterns = [
    # This url may be better represented at the root
    # path('goto/<uuid:link>/<uuid:user>/', whyness_crm.views.goto, name='crm-tracker'),
    path('crm/go/<uuid:link>/<uuid:user>/', views.goto, name='tracker'),
    path('crm/', views.dashboard, name='dashboard'),
    path('crm/<int:dataset_id>/', views.dashboard, name='dashboard'),
    path('crm/<int:dataset_id>/<int:message_id>/', views.dashboard, name='dashboard'),
    path('crm/app-aggregate/', views.app_aggregate, name='app-aggregate'),
    path('crm/trackers/', views.trackers, name='trackers'),
    path('crm/tracker/<int:tracker_id>/', views.tracker, name='tracker_item'),
    path('crm/user-status/', views.user_status, name='user-status'),
    path('crm/user-stories/', views.user_stories, name='user-stories'),
    path(
        'crm/user-stories-week/',
        views.user_stories_week,
        name='user-stories-week'
    ),
    path(
        'crm/user-transcript-readers-week/',
        views.user_transcript_readers_week,
        name='user-transcript-readers-week'
    ),
    path('crm/user-ai/', views.user_ai, name='user-ai'),
]
