#----------------------------------------------------------------------
# Whyness error serializers
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

"""
"""
from rest_framework import serializers

from whyness_error.models import ErrorLog

class ErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = (
            'create_date',
            'errorcode', 'errormessage',
        )
