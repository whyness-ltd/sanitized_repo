#----------------------------------------------------------------------
# Whyness user feedback urls
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from django.contrib import admin
from django.urls import path, include
from whyness_userfeedback import views
from whyness_userfeedback_api import views as admin_views

app_name="whyness_userfeedback"
urlpatterns = [
    path('feedback/<uuid:xref>/', views.userfeedback, name='user-feedback'),
    path(
        'feedback/values/',
        admin_views.userfeedback_values,
        name='user-feedback-values'
    ),
    path(
        'feedback/strengths/',
        admin_views.userfeedback_strengths,
        name='user-feedback-strengths'
    ),
    path(
        'feedback/impacts/',
        admin_views.userfeedback_impacts,
        name='user-feedback-impacts'
    ),
    path(
        'feedback/summary/',
        views.feedback_summary,
        name='feedback-summary'
    ),
]

