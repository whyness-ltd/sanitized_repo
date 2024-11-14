#----------------------------------------------------------------------
# Whyness prospect serializers
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from rest_framework import serializers
from whyness_prospect.models import Prospect

class ProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prospect
        fields = [
            'id',
            'name',
            'email',
            'status',
        ]
        read_only_fields = [
            'id',
            'status',
        ]

