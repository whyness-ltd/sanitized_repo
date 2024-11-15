#----------------------------------------------------------------------
# Whyness settings
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

"""
Django settings for whyness_django project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://REMOVED

For the full list of settings and their values, see
https://REMOVED
"""

import os
import boto3
from pathlib import Path
from corsheaders.defaults import default_headers

# Build config is either PROD or DEV
# Used by whyness_django.models.Audio
BUILD_CONFIG = os.environ['BUILD_CONFIG']
BUILD_PROD = "PROD"
BUILD_DEV = "DEV"

VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_REVISION = 0
VERSION_REVISION = 0

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TMP_DIR = '/tmp'
FFMPEG = None
if os.path.isfile('/usr/bin/ffmpeg'):
    FFMPEG = '/usr/bin/ffmpeg'
elif os.path.isfile('/usr/local/bin/ffmpeg'):
    FFMPEG = '/usr/local/bin/ffmpeg'

SITE_ID = 1
SITE_TITLE = 'WHYNESS Django Admin'
SITE_DESCRIPTION = 'WHYNESS Django Admin and API server'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'whyness-django'
AWS_QUERYSTRING_AUTH = False
AWS_S3_USE_SSL = True
# https://REMOVED
AWS_S3_ENDPOINT_URL = 'https://REMOVED'
AWS_DEFAULT_REGION = 'eu-west-2'
AWS_REGION_NAME  = os.environ['AWS_REGION_NAME']
AWS_DEFAULT_ACL = None
AWS_STS_REGIONAL_ENDPOINTS = 'regional'

LOGIN_REDIRECT_URL ='home'
LOGOUT_REDIRECT_URL = 'home'
ADMIN_PASSWORD_RESET = 'admin_password_reset'

# Email
ADMINS = [('Alan Hicks', 'email@REMOVED')]
DEFAULT_FROM_EMAIL = 'email@REMOVED'
SERVER_EMAIL = 'email@REMOVED'
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

# Mixpanel
MIXPANEL_PROJECT_ID = 2780485
MIXPANEL_SERVICE_ACCOUNT = os.environ['MIXPANEL_SERVICE_ACCOUNT']
MIXPANEL_SERVICE_PASSWORD = os.environ['MIXPANEL_SERVICE_PASSWORD']

# Secrets in Parameter store
def get_aws_parameter(param_name):
    ssm = boto3.client('ssm', region_name=AWS_REGION_NAME)
    try:
        Parameter = ssm.get_parameter(Name=param_name, WithDecryption=True)
        return Parameter['Parameter']['Value']
    except ssm.exceptions.ParameterNotFound:
        msg = "Unable to get parameter: {}".format(param_name)
        print(msg)
        return None
    except BaseException as err:
        msg = "Unexpected error getting parameter: {}: {}".format(param_name, err)
        print(msg)
        return None



# Get Database password
db_pass = get_aws_parameter(f"RDS_PASSWORD_{BUILD_CONFIG}")
django_secret_key = get_aws_parameter(f"DJANGO_SECRET_KEY_{BUILD_CONFIG}")

# Quick-start development settings - unsuitable for production
# See https://REMOVED

# SECURITY WARNING: keep the secret key used in production secret!
if os.environ.get('DJANGO_SECRET_KEY') is not None:
    SECRET_KEY = "REMOVED"
else:  
    SECRET_KEY = "REMOVED"

# SECURITY WARNING: don't run with debug turned on in production!
if BUILD_CONFIG == BUILD_PROD:
    DEBUG = False
else:
    DEBUG = True
    SITE_TITLE = "{} - dev".format(SITE_TITLE)

OTP_TOTP_ISSUER = SITE_TITLE

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = [
    "https://REMOVED",
    "https://REMOVED",
    "http://localhost:8080",
    "http://IP.REMOVED:9000",
    "http://IP.REMOVED:4200",
    "http://localhost:4200"
]

CORS_URLS_REGEX = r'^/api/.*$'

CORS_ALLOW_HEADERS = ['*']
#CORS_ALLOW_HEADERS = list(default_headers) + [
#    'x-session',
#    'x-csrftoken',
#    'origin',
#    'Authentication',
#    'Access-Control-Allow-Origin',
#]
CORS_EXPOSE_HEADERS = CORS_ALLOW_HEADERS
CORS_ALLOW_CREDENTIALS = False
SESSION_COOKIE_SAMESITE = 'lax'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = None
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False


# Application definition

INSTALLED_APPS = [
    'whyness_django',
    'whyness_crm',
    'whyness_error',
    'whyness_timesheet',
    'whyness_appgyver_polls',
    'whyness_crowdsource',
    'whyness_joblist',
    'whyness_mixpanel',
    'whyness_ml_models',
    'whyness_userfeedback',
    'whyness_userfeedback_api',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'storages',
    'oauth2_provider',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'whyness_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'whyness_django.wsgi.application'


# Database
# https://REMOVED

if os.environ.get('RDS_PASSWORD') is not None:
    RDS_PASSWORD = os.environ.get('RDS_PASSWORD')
else:  
    RDS_PASSWORD = db_pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': RDS_PASSWORD,
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.JSONParser',
    ]
}

# Password validation
# https://REMOVED

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

# Internationalization
# https://REMOVED

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://REMOVED

MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'media/'))
MEDIA_URL = 'https://REMOVED

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(__file__, '../static/')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = (
    ('css', os.path.join(BASE_DIR, 'static/css')),
    ('fonts', os.path.join(BASE_DIR, 'static/fonts')),
    ('images', os.path.join(BASE_DIR, 'static/images')),
    ('admin/js', os.path.join(BASE_DIR, 'static/admin/js')),
    ('admin/css', os.path.join(BASE_DIR, 'static/admin/css')),
    ('js', os.path.join(BASE_DIR, 'static/js')),
    ('filebrowser/js', os.path.join(BASE_DIR, 'static/filebrowser/js')),
    ('webfonts', os.path.join(BASE_DIR, 'static/webfonts')),
    ('mezzanine', os.path.join(BASE_DIR, 'static/mezzanine')),
)

# Default primary key field type
# https://REMOVED

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            # logging handler that outputs log messages to terminal
            'class': 'logging.StreamHandler',
            'level': 'DEBUG', # message level to be written to console
        },
        'syslog':{
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'email_backend': 'django.core.mail.backends.smtp.EmailBackend',
            'include_html': True,
        }
    },
    'loggers': {
        '': {
            'handlers': ['syslog', 'console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'WARNING',
        },
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db': {
            'handlers': ['syslog', 'console'],
            'level': 'WARNING',
            # django also has database level logging
        },
        'django.contrib.admin': {
            'handlers': ['syslog', 'console'],
            'level': 'DEBUG',
        },
        'whyness_appgyver_polls': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
        },
        'whyness_django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
        },
        'whyness_ml_models': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
        },
        'whyness_crm': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
        },
        'whyness_joblist': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
        },
        'whyness_mixpanel': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
        },
        'whyness_timesheet': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
        },
        'whyness_userfeedback_api': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
        },
        'django_otp': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
        },
        'whyness_crowdsource': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
        },
    }
}
