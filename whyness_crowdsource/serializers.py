#----------------------------------------------------------------------
# Whyness crowdsource serializers
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

from rest_framework import serializers

from whyness_crowdsource.models import StoryGrant
from whyness_crowdsource.models import Review
from whyness_crowdsource.models import ReviewReviewer
from whyness_crowdsource.models import ReviewStories
from whyness_crowdsource.models import ReviewFeedback
from whyness_crowdsource.models import ReviewSweetSpot

class StoryGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryGrant
        fields = [
            'is_granted',
            'create_date',
        ]
        read_only_fields = [
            'create_date',
        ]
#class StoryResultSerializer(serializers.ModelSerializer):
    #class Meta:
    #    model = StoryGrant
    #    fields = [
    #        'is_granted',
    #    ]
    #    read_only_fields = [
    #        'create_date',
    #    ]
class StoryReviewSerializer(serializers.ModelSerializer):
    """Story owner and Reviewer should be hidden from each other
    """
    class Meta:
        model = Review
        fields = [
            'status',
            'updated_date',
            'create_date',
        ]
        read_only_fields = [
            'updated_date',
            'create_date',
        ]
class StoryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'status',
            'updated_date',
            'create_date',
        ]
        read_only_fields = [
            'status',
            'updated_date',
            'create_date',
        ]
class StoryStoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewStories
        fields = [
            'review',
            'story',
            'create_date',
        ]
        read_only_fields = [
            'review',
            'story',
            'create_date',
        ]
class StoryStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'create_date',
        ]
        read_only_fields = [
            'create_date',
        ]

class ReviewReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReviewer
        fields = [
            'feedback',
            'create_date',
        ]
        read_only_fields = [
            'create_date',
        ]

class ReviewRejectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReviewer
        fields = [
            'review',
            'feedback',
            'create_date',
        ]
        read_only_fields = [
            'review',
            'feedback',
            'create_date',
        ]
class ReviewFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewFeedback
        fields = [
            'review',
            'feedback',
            'create_date',
        ]
        read_only_fields = [
            'review',
            'feedback',
            'create_date',
        ]
class ReviewSweetSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewSweetSpot
        fields = [
            'review',
            'value1', 'value2', 'value3',
            'valueother', 'valueconfidence',
            'strength1', 'strength2', 'strength3',
            'strengthother', 'strengthconfidence',
            'impact1', 'impact2', 'impact3',
            'impactother', 'impactconfidence',
            'create_date',
        ]
        read_only_fields = [
            'review',
            'create_date',
        ]
class ReviewCloseSerializer(serializers.ModelSerializer):
    sweetspot = ReviewSweetSpotSerializer
    feedback = ReviewFeedback

