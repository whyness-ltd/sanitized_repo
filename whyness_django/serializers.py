#----------------------------------------------------------------------
# Whyness serializers
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from rest_framework import serializers
from whyness_django.models import AuthUser
from whyness_django.models import Audio, Question
from whyness_django.models import ErrorLog
from whyness_django.models import UserAgent
from whyness_django.models import Profession, Role, TypeAttributes

class VersionSerializer(serializers.Serializer):
    major = serializers.IntegerField()
    minor = serializers.IntegerField()
    revision = serializers.IntegerField()
    version = serializers.CharField()
    production = serializers.BooleanField()
    class Meta:
        fields = [
            'major',
            'minor',
            'revision',
            'version',
            'production',
        ]
        read_only_fields = [
            'major',
            'minor',
            'revision',
            'version',
            'production',
        ]

class UserPWResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = [
            'id',
            'title',
        ]

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id',
            'title',
        ]
class TypeAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeAttributes
        fields = [
            'id',
            'title',
            'description',
        ]
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'question',
            'sort_order',
            'status',
        ]

class RepresentationalSystemSerializer(serializers.Serializer):
    visual = serializers.IntegerField()
    auditory = serializers.IntegerField()
    kinesthetic = serializers.IntegerField()
    auditory_digital = serializers.IntegerField()

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = [
            'id',
            'name',
            'email',
            'xref',
            'create_date',
        ]
        read_only_fields = [
            'id',
            'email',
            'xref',
            'uid',
            'status',
            'update_ip',
            'update_date',
            'create_date',
        ]

class UserProfileSerializer(serializers.Serializer):
    representational_system = RepresentationalSystemSerializer()

class UserStatusSerializer(serializers.Serializer):
    sweetspot_completed = serializers.BooleanField()
    dreamjob_completed = serializers.BooleanField()
    word_count = serializers.IntegerField()
    class Meta:
        fields = [
            'sweetspot_completed',
            'dreamjob_completed',
            'word_count',
        ]
        read_only_fields = [
            'sweetspot_completed',
            'dreamjob_completed',
            'word_count',
        ]

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = [
            'id',
            'question',
            'media',
            'transcript',
            'representational_system',
            'update_date',
            'create_date',
            'status',
        ]
        read_only_fields = [
            'id',
            'update_date',
            'create_date',
            'status',
        ]

class AudioResponseSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    class Meta:
        model = Audio
        fields = [
            'id',
            'question',
            'transcript',
            'representational_system',
            'update_date',
            'create_date',
            'status',
        ]

class ErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = [
            'id',
            'date',
            'errorcode', 'errormessage',
        ]

class UserAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAgent
        fields = [
            'id',
            'useragent',
        ]
