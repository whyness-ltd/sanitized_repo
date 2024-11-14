#----------------------------------------------------------------------
# Whyness crowdsource views
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
import logging

from django.http import Http404

from whyness_django.views import get_auth_user
from whyness_django.views import tracker_log, get_host_info
from whyness_django.models import AuthUser
from whyness_django.models import Audio
from whyness_django.models import TRANSCRIPT_STATUS_MBTI

from whyness_crowdsource.models import StoryGrant
from whyness_crowdsource.models import Review
from whyness_crowdsource.models import ReviewStories
from whyness_crowdsource.models import ReviewReviewer
from whyness_crowdsource.models import ReviewFeedback
from whyness_crowdsource.models import ReviewSweetSpot

from whyness_crowdsource.models import REVIEW_INACTIVE
from whyness_crowdsource.models import REVIEW_OPEN
from whyness_crowdsource.models import REVIEW_COMPLETED
from whyness_crowdsource.models import REVIEW_REJECTED
from whyness_crowdsource.models import REVIEW_DELETED
from whyness_crowdsource.models import STORIES_IN_PROGRESS

from whyness_crowdsource.serializers import StoryGrantSerializer
from whyness_crowdsource.serializers import StoryReviewSerializer
from whyness_crowdsource.serializers import StoryStatusSerializer
from whyness_crowdsource.serializers import StoryStoriesSerializer
from whyness_crowdsource.serializers import StoryStartSerializer
from whyness_crowdsource.serializers import ReviewFeedbackSerializer
from whyness_crowdsource.serializers import ReviewReviewerSerializer
from whyness_crowdsource.serializers import ReviewRejectSerializer
from whyness_crowdsource.serializers import ReviewCloseSerializer

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

MIN_STORIES = 3

logger = logging.getLogger(__name__)

def get_user_is_granted(user):
    """Returns the latest grant, or the default grant(False)"""
    grant = StoryGrant.objects.filter(user=user).order_by('-create_date')
    if grant:
        grant = grant[0]
    else:
        grant = StoryGrant(user=user)
    return grant.is_granted

def get_user_review(user):
    """Returns a review for a user, or None"""
    review = Review.objects.filter(user=user, status=REVIEW_OPEN)
    if review:
        review = review[0]
    return review

def get_reviewer_review(user):
    """Returns a review for a reviewer, or None"""
    review = ReviewReviewer.objects.filter(reviewer=user, status=REVIEW_OPEN)
    if review:
        review = review[0].review
    return review

class ApiStoryGrant(APIView):
    """Grant permission to croudsource story feedback"""
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Return latest permission, or false
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='croudsource_story_grant',
            request=request,
            user=user,
        )

        data = StoryGrant.objects.filter(user=user).order_by('-create_date')
        if data:
            data = data[0]
        else:
            data = StoryGrant(user=user)

        return Response(StoryGrantSerializer(data).data)

    def post(self, request, format=None):
        """
        Post
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='croudsource_story_grant',
            request=request,
            user=user,
        )

        try:
            data_response = StoryGrantSerializer(data=request.data)
        except Exception as err:
            msg = "An Error occured serializing story grant: {}".format(err)
            logger.warning(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        if data_response.is_valid():
            (remote_addr, remote_host) = get_host_info(request)
            result = data_response.save(user=user, update_ip=remote_addr)
        else:
            msg = "An Error occured saving story grant: {}".format(err)
            logger.error(msg)
            return Response(data_response.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data_response.data)

class ApiStoryStart(APIView):
    """Story Start
    A story owner must have granted access
    A story owner must not have an open review
    A story owner must have at least three stories available
    Returns:
    - error:
        CROWDSOURCE_NOT_GRANTED
        CROWDSOURCE_REVIEW_OPEN
        NOT_ENOUGH_STORIES
    - status:
        NOT_STARTED
        STARTED
    """
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        Post a signal to start reviewing a story owners stories
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='croudsource_story_start',
            request=request,
            user=user,
        )
        ret_msg = {'status': 'NOT_STARTED'}

        grant = get_user_is_granted(user)
        if not grant:
            ret_msg['error'] = 'CROWDSOURCE_NOT_GRANTED'
            return Response(ret_msg, status=status.HTTP_400_BAD_REQUEST)
        review = get_user_review(user)
        if review:
            ret_msg['error'] = 'CROWDSOURCE_REVIEW_OPEN'
            return Response(ret_msg, status=status.HTTP_400_BAD_REQUEST)

        raw_sql = """
        SELECT audio.*
        FROM whyness_django_audio AS audio
        WHERE user_id = %s
        AND status = %s
        AND id NOT IN (
            SELECT rs.story_id
            FROM whyness_crowdsource_reviewstories AS rs
            INNER JOIN whyness_crowdsource_review as r
            ON r.id = rs.review_id
            WHERE r.user_id = audio.user_id
            AND r.status < %s
        )
        """
        stories = Audio.objects.raw(
            raw_sql, [
                user.id,
                TRANSCRIPT_STATUS_MBTI,
                STORIES_IN_PROGRESS,
            ] )

        if len(stories) < MIN_STORIES:
            ret_msg['error'] = 'NOT_ENOUGH_STORIES'
            return Response(ret_msg, status=status.HTTP_400_BAD_REQUEST)

        # Create a review
        review = Review(user=user, status=REVIEW_OPEN)
        review.save()
        # Add stories to review
        for story in stories:
            new_story = ReviewStories(review=review, story=story)
            new_story.save()

        ret_msg = {'status': 'STARTED'}
        return Response(ret_msg, status=status.HTTP_200_OK)

class ApiStoryStatus(APIView):
    """User"""
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Return
        error:
            CROWDSOURCE_REVIEW_NOT_OPEN
        {
            "status": true,
            "updated_date": date,
            "create_date": date
        }

        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='croudsource_story_status',
            request=request,
            user=user,
        )

        ret_msg = {}
        data = get_user_review(user)
        if not data:
            ret_msg['error'] = 'CROWDSOURCE_REVIEW_NOT_OPEN'
            return Response(ret_msg, status=status.HTTP_400_BAD_REQUEST)

        return Response(StoryStatusSerializer(data).data)

class ApiStoryStories(APIView):
    """Stories open for review,
    available to story owners"""
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Return
        error:
            CROWDSOURCE_REVIEW_NOT_OPEN
        data:
        [
            {stories...},
        ]
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='croudsource_story_stories',
            request=request,
            user=user,
        )

        ret_msg = {}
        review = get_user_review(user)
        if not review:
            ret_msg['error'] = 'CROWDSOURCE_REVIEW_NOT_OPEN'
            return Response(ret_msg, status=status.HTTP_400_BAD_REQUEST)

        data = ReviewStories.objects.filter(review=review)

        return Response(StoryStoriesSerializer(data, many=True).data)

class ApiReviewStatus(APIView):
    """Status of the current review"""
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Return
        error:
            CROWDSOURCE_REVIEW_NOT_OPEN
        review:
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='croudsource_story_stories',
            request=request,
            user=user,
        )

        ret_msg = {}
        review = get_reviewer_review(user)
        if not review:
            ret_msg['error'] = 'CROWDSOURCE_REVIEW_NOT_OPEN'
            return Response(ret_msg, status=status.HTTP_400_BAD_REQUEST)

        data = review

        return Response(ReviewReviewerSerializer(data).data)

class ApiReviewStories(APIView):
    """Stories open for review,
    available to reviewers"""
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Return
        error:
            CROWDSOURCE_REVIEW_NOT_OPEN
        data:
        [
            {stories...},
        ]
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='croudsource_story_stories',
            request=request,
            user=user,
        )

        ret_msg = {}
        review = get_reviewer_review(user)
        if not review:
            ret_msg['error'] = 'CROWDSOURCE_REVIEW_NOT_OPEN'
            return Response(ret_msg, status=status.HTTP_400_BAD_REQUEST)

        data = ReviewStories.objects.filter(review=review)

        return Response(StoryStoriesSerializer(data, many=True).data)

class ApiReviewStart(APIView):
    """Review Start
    A reviewer must not have an open review
    """
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        Post a signal to start reviewing a story owners stories
        error:
            CROWDSOURCE_REVIEW_OPEN
            CROWDSOURCE_NO_REVIEWS
        status:
            NOT_STARTED
            STARTED
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='croudsource_review_start',
            request=request,
            user=user,
        )
        ret_msg = {'status': 'NOT_STARTED'}

        review = get_reviewer_review(user)
        if review:
            ret_msg['error'] = 'CROWDSOURCE_REVIEW_OPEN'
            return Response(ret_msg, status=status.HTTP_400_BAD_REQUEST)

        reviews = Review.objects.filter(
            status=REVIEW_OPEN
        ).exclude(
            user=user
        ).order_by('-create_date')
        # TODO
        # Get highest priority reviews first
        if len(reviews) == 0:
            ret_msg['error'] = 'CROWDSOURCE_NO_REVIEWS'
            return Response(ret_msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            review = reviews[0]
        # Create a review
        data = ReviewReviewer(
            review=review,
            reviewer=user,
            status=REVIEW_OPEN
        )
        data.save()

        ret_msg = {'status': 'STARTED'}
        return Response(ret_msg, status=status.HTTP_200_OK)

class ApiReviewReject(APIView):
    """Reject a Review"""
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        Post a rejection of a review
        error:
            CROWDSOURCE_REVIEW_NOT_OPEN
        status:
            NOT_REJECTED
            REJECTED
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='croudsource_review_reject',
            request=request,
            user=user,
        )

        ret_msg = {'status': 'NOT_REJECTED'}

        review = get_reviewer_review(user)
        if not review:
            ret_msg['error'] = 'CROWDSOURCE_REVIEW_NOT_OPEN'
            return Response(ret_msg, status=status.HTTP_400_BAD_REQUEST)

        review.feedback = request.POST['feedback']
        try:
            review.save()
        except Exception as err:
            msg = "An Error occured rejecting this review: {}".format(err)
            logger.warning(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        return Response(ReviewSweetSpotSerializer(result).data)

class ApiReviewClose(APIView):
    """Close a Review with a Sweet Spot and optional feedback"""
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        Post sweet spot from a reviewer
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='croudsource_review_sweetspot',
            request=request,
            user=user,
        )

        try:
            user_response = ReviewCloseSerializer(instance=user, data=request.data)
        except Exception as err:
            msg = "An Error occured serializing review sweetspot: {}".format(err)
            logger.warning(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        if user_response.is_valid():
            (remote_addr, remote_host) = get_host_info(request)
            result = user_response.save(user=user, update_ip=remote_addr)
        else:
            msg = "An Error occured saving review sweetspot: {}".format(err)
            logger.warning(msg)
            return Response(user_response.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(ReviewSweetSpotSerializer(result).data)


class ApiStoryReviews(APIView):
    """Story reviews"""
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Return
        error:
            CROWDSOURCE_NO_REVIEWS
        reviews:
        [
            {reviews...},
        ]
        """
        user = get_auth_user(request)
        if not user:
            raise Http404

        tracker_log(
            activity='croudsource_story_reviews',
            request=request,
            user=user,
        )

        ret_msg = {}
        data = ReviewReviewer.objects.filter(
            review__review__user=user
        )
        if not reviews:
            ret_msg['error'] = 'CROWDSOURCE_NO_REVIEWS'
            return Response(ret_msg, status=status.HTTP_400_BAD_REQUEST)

        data = ReviewStories.objects.filter(review=review)

        return Response(StoryReviewSerializer(data, many=True).data)

