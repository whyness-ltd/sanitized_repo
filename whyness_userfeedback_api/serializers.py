#----------------------------------------------------------------------
# Whyness user feedback api serializers
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from rest_framework import serializers

class UserFeedbackValueSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=100)
    value_count = serializers.IntegerField()
    class Meta:
        fields = [
            'value',
            'value_count',
        ]
        read_only_fields = [
            'value',
            'value_count',
        ]

class UserFeedbackStrengthSerializer(serializers.Serializer):
    strength = serializers.CharField(max_length=100)
    strength_count = serializers.IntegerField()
    class Meta:
        fields = [
            'strength',
            'strength_count',
        ]
        read_only_fields = [
            'strength',
            'strength_count',
        ]

class UserFeedbackImpactSerializer(serializers.Serializer):
    impact = serializers.CharField(max_length=100)
    impact_count = serializers.IntegerField()
    class Meta:
        fields = [
            'impact',
            'impact_count',
        ]
        read_only_fields = [
            'impact',
            'impact_count',
        ]

class UserFeedbackConfidenceSerializer(serializers.Serializer):
    valueconfidence = serializers.CharField(max_length=100)
    valueconfidence_count = serializers.IntegerField()
    strengthconfidence = serializers.CharField(max_length=100)
    strengthconfidence_count = serializers.IntegerField()
    impactconfidence = serializers.CharField(max_length=100)
    impactconfidence_count = serializers.IntegerField()
    class Meta:
        fields = [
            'valueconfidence',
            'valueconfidence_count',
            'strengthconfidence',
            'strengthconfidence_count',
            'impactconfidence',
            'impactconfidence_count',
        ]
        read_only_fields = [
            'valueconfidence',
            'valueconfidence_count',
            'strengthconfidence',
            'strengthconfidence_count',
            'impactconfidence',
            'impactconfidence_count',
        ]

class UserFeedbackSerializer(serializers.Serializer):
    values = UserFeedbackValueSerializer(many=True)
    strengths = UserFeedbackStrengthSerializer(many=True)
    impacts = UserFeedbackImpactSerializer(many=True)
    confidence = UserFeedbackConfidenceSerializer(many=True)
