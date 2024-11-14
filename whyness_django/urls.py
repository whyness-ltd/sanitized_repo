#----------------------------------------------------------------------
# Whyness urls
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

"""whyness_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://REMOVED
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework import routers
from . import views
from whyness_crowdsource import urls as crowdsource_urls
from whyness_crm import views as crm_views
from whyness_error import urls as error_urls
from whyness_ml_models import urls as ml_models_urls
from whyness_timesheet import views as timesheet_views
from whyness_appgyver_polls import urls as appgyver_polls_urls
from whyness_joblist import urls as joblist_api_urls
from whyness_userfeedback import urls as userfeedback_urls
from whyness_userfeedback_api import urls as userfeedback_api_urls
from django_otp.views import LoginView as django_otp_login_view
from django_otp.forms import OTPAuthenticationForm
from django_otp.admin import OTPAdminAuthenticationForm

router = routers.DefaultRouter()

urlpatterns = [
    path("", views.home, name="home"),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path("media", views.media_list, name="media_list"),
    path("media/<int:id>/", views.media_item, name="media_item"),

    path('api/version/', views.ApiVersion.as_view(), name='version'),
    path('api/v1/media/<int:id>/', views.ApiMedia.as_view(), name='api-media'),
    path('api/v1/media/', views.ApiMedia.as_view(), name='api-media'),
    path('api/v1/question/<int:id>/', views.ApiQuestion.as_view(), name='api-media'),
    path('api/v1/question/', views.ApiQuestion.as_view(), name='api-question'),
    path('api/v1/profession/<int:id>/', views.ApiProfession.as_view(), name='api-profession'),
    path('api/v1/profession/', views.ApiProfession.as_view(), name='api-profession'),
    path('api/v1/role/<int:id>/', views.ApiRole.as_view(), name='api-role'),
    path('api/v1/role/', views.ApiRole.as_view(), name='api-role'),
    path('api/v1/typeattributes/<int:id>/', views.ApiTypeAttributes.as_view(), name='api-typeattributes'),
    path('api/v1/typeattributes/', views.ApiTypeAttributes.as_view(), name='api-typeattributes'),
    path('api/v1/typeattributes/<int:id>/roles/', views.ApiTypeAttributesRoles.as_view(), name='api-typeattributeroles'),
    path('api/v1/user/', views.ApiUser.as_view(), name='api-user'),
    path(
        'api/v1/user/reset_password/',
        views.ApiUserPWReset.as_view(),
        name='api-user-reset-password'
    ),
    path('api/v1/user/profile/', views.ApiUserProfile.as_view(), name='api-user-profile'),
    path('api/v1/user/status/', views.ApiUserStatus.as_view(), name='api-user-status'),
    path('api/v1/user/profile/<str:id>/', views.ApiUserProfile.as_view(), name='api-user-profile'),

    path(
        'admin/password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='admin_password_reset',
    ),
    path(
        'admin/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path(
        'accounts/login/',
        django_otp_login_view.as_view(authentication_form=OTPAdminAuthenticationForm),
        name="django-otp-login"
    ),
    path('admin/', include('whyness_crm.urls', namespace="whyness_crm")),
    path('admin/', include('whyness_timesheet.urls')),
    path("admin/login/", views.home, name="admin-login"),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    path('api/', include(appgyver_polls_urls)),
    path('api/', include(crowdsource_urls)),
    path('api/', include(error_urls)),
    path('api/', include(joblist_api_urls)),
    path('api/', include(ml_models_urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('user/', include(userfeedback_urls)),
    path('api/', include(userfeedback_api_urls)),
    path('goto/<uuid:link>/<uuid:user>/', crm_views.goto, name='crm-tracker'),
    path('', include('django.contrib.flatpages.urls')),
]
