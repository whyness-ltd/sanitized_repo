#----------------------------------------------------------------------
# Whyness serializers
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from rest_framework import serializers
from whyness_django.models import UserAgent
from whyness_appgyver_polls.models import DreamJob
from whyness_appgyver_polls.models import SweetSpotValue
from whyness_appgyver_polls.models import SweetSpotStrength
from whyness_appgyver_polls.models import SweetSpotImpact
from whyness_appgyver_polls.models import SweetSpot

class DreamJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DreamJob
        fields = [
            'id', 'user', 'ip',
            'role1', 'role2', 'role3',
            'roleother', 'roleconfidence',
            'profession1', 'profession2', 'profession3',
            'professionother', 'professionconfidence',
            'company_size', 'office_culture', 'create_date',
        ]
        read_only_fields = [
            'id', 'user', 'ip',
            'create_date',
        ]
        extra_kwargs = {
            # Tell DRF that the link field is not required.
            'roleother': {
                'required': False,
                'allow_blank': True,
            },
            'professionother': {
                'required': False,
                'allow_blank': True,
            },
        }

class SweetSpotValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SweetSpotValue
        fields = ['id', 'title']
        read_only_fields = ['id', 'title']
class SweetSpotStrengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = SweetSpotStrength
        fields = ['id', 'title']
        read_only_fields = ['id', 'title']
class SweetSpotImpactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SweetSpotImpact
        fields = ['id', 'title']
        read_only_fields = ['id', 'title']

class SweetSpotSerializer(serializers.ModelSerializer):
    def validate_valueother(self, value):
        if not value:
            value=""
        return value
    def validate_strengthother(self, value):
        if not value:
            value=""
        return value
    def validate_impactother(self, value):
        if not value:
            value=""
        return value
    def validate(self, data):
        """
        Check that start is before finish.
        """
        if 'valueother' not in data:
            data['valueother'] = ""
        if 'strengthother' not in data:
            data['strengthother'] = ""
        if 'impactother' not in data:
            data['impactother'] = ""
        return data
    class Meta:
        model = SweetSpot
        fields = [
            'id', 'user', 'ip',
            'value1', 'value2', 'value3',
            'valueother', 'valueconfidence',
            'strength1', 'strength2', 'strength3',
            'strengthother', 'strengthconfidence',
            'impact1', 'impact2', 'impact3',
            'impactother', 'impactconfidence',
            'create_date',
        ]
        read_only_fields = [
            'id', 'user', 'ip',
            'create_date',
        ]
        extra_kwargs = {
            # Tell DRF that the link field is not required.
            'valueother': {
                'required': False,
                'allow_blank': True,
            },
            'strengthother': {
                'required': False,
                'allow_blank': True,
            },
            'impactother': {
                'required': False,
                'allow_blank': True,
            },
        }
