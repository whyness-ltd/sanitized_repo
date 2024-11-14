#----------------------------------------------------------------------
# Whyness serializers
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from rest_framework import serializers
from whyness_django.models import UserAgent

from whyness_ml_models.models import MBTI

class MBTISerializer(serializers.ModelSerializer):
    word_count = serializers.IntegerField()
    class Meta:
        model = MBTI
        fields = [
            'id',
            'IE',
            'NS',
            'TF',
            'PJ',
            'word_count',
            'create_date',
        ]
        read_only_fields = [
            'id',
            'create_date',
            'word_count',
        ]
