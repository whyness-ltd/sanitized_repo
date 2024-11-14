#----------------------------------------------------------------------
# Whyness crm views
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
import logging
import datetime
import uuid

from django import template
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db import connection
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.template import Context, Template
from django.urls import reverse
from django.utils.html import format_html

from html.parser import HTMLParser

from whyness_django.models import AuthUser
from whyness_django.views import get_host_info

from whyness_crm.models import Contact
from whyness_crm.models import ContactRecord
from whyness_crm.models import AuthUserContactRecord
from whyness_crm.models import Message
from whyness_crm.models import UserSQL
from whyness_crm.models import TrackerDestination
from whyness_crm.models import AuthUserTrackerClick
from whyness_crm.models import ContactTrackerClick

from whyness_crm.models import STATUS_ACTIVE
from whyness_crm.models import MESSAGE_STATUS_ACTIVE

from whyness_crm.models import CONTACT_PROSPECT
from whyness_crm.models import CONTACT_USER

from whyness_mixpanel.models import Event

UUID_NULL = uuid.UUID('00000000-0000-0000-0000-000000000000')

register = template.Library()

logger = logging.getLogger(__name__)

class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, data):
        self.text += data

def send_message_via_email(message, user, contact_type):
    """Send a message via email to a user"""
    msg = "Sending message <{}> to: {}".format(message, user)
    logger.debug(msg)
    if user:
        if not hasattr(user, 'name'):
            # Convert Django to oAuth name
            name = '{} {}'.format(
                user.first_name,
                user.last_name
            )
            user.name = name
            user.xref = UUID_NULL
        context = {
            'user': user,
        }

        filter = HTMLFilter()
        tpl_txt = filter.feed(message.message_html)
        date_now = datetime.date.today()

        try:
            context = Context(context)
            template = Template(tpl_txt)
            msg_text = template.render(context)
            template = Template('{{% load crm_link %}}{}'.format(message.message_html))
            msg_html = template.render(context)
            subject = message.title
            from_email = message.from_user.email
            to_email = user.email
            msg = EmailMultiAlternatives(subject, msg_text, from_email, [to_email])
            msg.attach_alternative(msg_html, 'text/html')
            msg.send()
            msg = "Message sent to: {}".format(to_email)
            logger.debug(msg)
        except Exception as err:
            msg = "Could not send message: {} to: {}:".format(
                message.title,
                user.email,
                err,
            )
            logger.debug(msg)
        if not hasattr(user, 'first_name'):
            # Test for User is not staff/django - send to me
            try:
                if contact_type == CONTACT_PROSPECT:
                    record = ContactRecord(
                        contact=user,
                        message=message,
                        sent_date=date_now,
                        message_status=MESSAGE_STATUS_ACTIVE,
                        status=STATUS_ACTIVE,
                    )
                    record.save()
                elif contact_type == CONTACT_USER:
                    record = AuthUserContactRecord(
                        contact=user,
                        message=message,
                        sent_date=date_now,
                        message_status=MESSAGE_STATUS_ACTIVE,
                        status=STATUS_ACTIVE,
                    )
                    record.save()
            except Exception as err:
                msg = "Could not record sending message: {} to: {}:".format(
                    message.title,
                    user.email,
                    err,
                )
                logger.debug(msg)

def dashboard(request, dataset_id=0, message_id=0):
    """Dashboard
    Choose dataset and message to first test then distribute
    Filter by message and or tracker
    """
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('home'))
    if not request.user.is_verified:
        return HttpResponseRedirect(reverse('home'))
    limit = 0
    if 'sendtome' in request.POST:
        limit = 10000
    elif 'sendtoall' in request.POST:
        limit = 10000
    else:
        limit = 200
    dataset = None
    message = None
    tracker = None
    contacts = None
    contacts_count = 0
    users = None
    users_count = 0
    custom_result = None
    custom_columns = None
    filter_message = None
    filter_tracker = None
    trackers_filter_type = None
    messages_filter_type = None

    # messages_filter_type
    # all
    # messaged - those who have been sent a message
    # unmessaged - those who have not been sent a message

    # trackers_filter_type
    # all
    # tracked - those who have clicked a link
    # untracked - those who have not clicked a link
    if request.method == "POST":
        if 'trackers-filter-type' in request.POST:
            trackers_filter_type = request.POST['trackers-filter-type']
        if 'filter-messages-type' in request.POST:
            messages_filter_type = request.POST['filter-messages-type']
            msg = 'messages_filter_type: {}'.format(messages_filter_type)
            logger.debug(msg)
        if 'filter-messages' in request.POST:
            filter_message_id = int(request.POST['filter-messages'])
            if filter_message_id:
                msg = 'filter-messages: {}'.format(filter_message_id)
                logger.debug(msg)
                filter_message = Message.objects.get(pk=filter_message_id)
                msg = 'filter_message: {}'.format(filter_message.title)
                logger.debug(msg)
        if 'filter-trackers' in request.POST:
            filter_tracker_id = int(request.POST['filter-trackers'])
            if filter_tracker_id:
                filter_tracker = TrackerDestination.objects.get(pk=filter_tracker_id)
                msg = 'filter_tracker: {}'.format(filter_tracker.title)
                logger.debug(msg)

    datasets = UserSQL.objects.filter(
        status=STATUS_ACTIVE
    ).order_by('title')
    crm_messages = Message.objects.filter(
        status=STATUS_ACTIVE
    ).order_by('title')
    trackers = TrackerDestination.objects.filter(
        status=STATUS_ACTIVE
    ).order_by('title')

    if dataset_id:
        dataset = UserSQL.objects.get(
            status=STATUS_ACTIVE,
            pk=dataset_id,
        )
        # Fetch records
        sql_and_message = ""
        sql_and_filter = ""
        if filter_message:
            if messages_filter_type == "unmessaged":
                # The message_id is sanitsed as int via url path
                if dataset.contact_type == CONTACT_PROSPECT:
                    sql_and_message = """
                        AND c.id NOT IN
                        (SELECT cr.contact_id
                        FROM whyness_crm_contactrecord AS cr
                        WHERE cr.contact_id = c.id
                        AND cr.message_id = {})
                    """.format(filter_message.id)
                elif dataset.contact_type == CONTACT_USER:
                    sql_and_message = """
                        AND c.id NOT IN
                        (SELECT cr.contact_id
                        FROM whyness_crm_authusercontactrecord AS cr
                        WHERE cr.contact_id = c.id
                        AND cr.message_id = {})
                    """.format(filter_message.id)
            elif messages_filter_type == "messaged":
                # The message_id is sanitsed as int via url path
                if dataset.contact_type == CONTACT_PROSPECT:
                    sql_and_message = """
                        AND c.id IN
                        (SELECT cr.contact_id
                        FROM whyness_crm_contactrecord AS cr
                        WHERE cr.contact_id = c.id
                        AND cr.message_id = {})
                    """.format(filter_message.id)
                elif dataset.contact_type == CONTACT_USER:
                    sql_and_message = """
                        AND c.id IN
                        (SELECT cr.contact_id
                        FROM whyness_crm_authusercontactrecord AS cr
                        WHERE cr.contact_id = c.id
                        AND cr.message_id = {})
                    """.format(filter_message.id)
        if filter_tracker:
            #select id, title from whyness_crm_trackerdestination
            # whyness_crm_authusertrackerclick
            # whyness_crm_contacttrackerclick
            # id
            # contact_id     | integer | not null |
            # destination_id | integer | not null |

            if trackers_filter_type == "untracked":
                if dataset.contact_type == CONTACT_PROSPECT:
                    sql_and_filter = """
                        AND c.id NOT IN
                        (SELECT ct.contact_id
                        FROM whyness_crm_contacttrackerclick AS ct
                        WHERE ct.contact_id = c.id
                        AND ct.destination_id = {})
                    """.format(filter_tracker.id)
                elif dataset.contact_type == CONTACT_USER:
                    sql_and_filter = """
                        AND c.id NOT IN
                        (SELECT ct.contact_id
                        FROM whyness_crm_authusercontactrecord AS ct
                        WHERE ct.contact_id = c.id
                        AND ct.destination_id = {})
                    """.format(filter_tracker.id)
            elif trackers_filter_type == "tracked":
                if dataset.contact_type == CONTACT_PROSPECT:
                    sql_and_filter = """
                        AND c.id IN
                        (SELECT ct.contact_id
                        FROM whyness_crm_contacttrackerclick AS ct
                        WHERE ct.contact_id = c.id
                        AND ct.destination_id = {})
                    """.format(filter_tracker.id)
                elif dataset.contact_type == CONTACT_USER:
                    sql_and_filter = """
                        AND c.id IN
                        (SELECT ct.contact_id
                        FROM whyness_crm_authusercontactrecord AS ct
                        WHERE ct.contact_id = c.id
                        AND ct.destination_id = {})
                    """.format(filter_tracker.id)
        # Fetch count
        raw_sql = "SELECT count(*) {} {} {}".format(
            dataset.sql,
            sql_and_message,
            sql_and_filter,
        )
        with connection.cursor() as cursor:
            cursor.execute(raw_sql)
            row = cursor.fetchone()

        # Select count
        if dataset.contact_type == CONTACT_PROSPECT:
            contacts_count = row[0]
        else:
            users_count = row[0]

        # Fetch custom result
        raw_sql = "{} {} {} {} ORDER BY 3 LIMIT {}".format(
            dataset.sql_select,
            dataset.sql,
            sql_and_message,
            sql_and_filter,
            limit
        )
        # Select data
        if dataset.contact_type == CONTACT_PROSPECT:
            contacts = Contact.objects.raw(raw_sql)
        else:
            users = AuthUser.objects.raw(raw_sql)

        logger.debug(raw_sql)
        with connection.cursor() as cursor:
            cursor.execute(raw_sql)
            custom_columns = [col[0] for col in cursor.description]
            custom_result = cursor.fetchall()
    else:
        # Prospects
        dataset = UserSQL.objects.get(
            slug='all-active-prospects',
            contact_type=CONTACT_PROSPECT,
            status=STATUS_ACTIVE
        )
        raw_sql = "SELECT count(*) {}".format(dataset.sql)
        logger.debug(raw_sql)
        with connection.cursor() as cursor:
            cursor.execute(raw_sql)
            row = cursor.fetchone()
            contacts_count = row[0]
        raw_sql = "{} {} LIMIT {}".format(dataset.sql_select, dataset.sql, limit)
        logger.debug(raw_sql)
        contacts = Contact.objects.raw(raw_sql)
        # Registered users
        dataset = UserSQL.objects.get(
            slug='all-active-users',
            contact_type=CONTACT_USER,
            status=STATUS_ACTIVE
        )
        raw_sql = "SELECT count(*) {}".format(dataset.sql)
        logger.debug(raw_sql)
        with connection.cursor() as cursor:
            cursor.execute(raw_sql)
            row = cursor.fetchone()
            users_count = row[0]
        raw_sql = "{} {} LIMIT {}".format(dataset.sql_select, dataset.sql, limit)
        logger.debug(raw_sql)
        users = AuthUser.objects.raw(raw_sql)
    if message_id:
        message = Message.objects.get(
            status=STATUS_ACTIVE,
            pk=message_id,
        )

    if request.method == 'POST':
        msg = "Posted"
        logger.debug(msg)
        target_users = None
        contact_type = None
        if 'sendtome' in request.POST:
            target_users = [request.user, ]
        if 'sendtoall' in request.POST:
            contact_type = dataset.contact_type
            if dataset.contact_type == CONTACT_PROSPECT:
                target_users = contacts
            else:
                target_users = users
        if target_users and message_id:
            for user in target_users:
                logger.debug(user)
                send_message_via_email(
                    message=message,
                    user=user,
                    contact_type=dataset.contact_type,
                )
            msg = "Messages sent"
            messages.add_message(request, messages.INFO, msg)

    context = {
        'contacts': contacts,
        'contacts_count': contacts_count,
        'users': users,
        'users_count': users_count,
        'limit': limit,
        'datasets': datasets,
        'dataset': dataset,
        'dataset_id': dataset_id,
        'crm_messages': crm_messages,
        'message': message,
        'message_id': message_id,
        'trackers': trackers,
        'tracker': tracker,
        'custom_result': custom_result,
        'custom_columns': custom_columns,
        'messages_filter_type': messages_filter_type,
        'trackers_filter_type': trackers_filter_type,
        'filter_message': filter_message,
        'filter_tracker': filter_tracker,
    }
    return render(request, 'whyness_crm/dashboard.html', context)

def trackers(request, tracker_id=0):
    """Tracker Dashboard"""
    limit = 50
    tracker = None

    trackers = TrackerDestination.objects.filter(
        status=STATUS_ACTIVE
    ).order_by('title')

    context = {
        'limit': limit,
        'trackers': trackers,
    }
    return render(request, 'whyness_crm/tracker_index.html', context)

def tracker(request, tracker_id):
    try:
        tracker = TrackerDestination.objects.get(
            status=STATUS_ACTIVE,
            pk=tracker_id,
        )
    except TrackerDestination.DoesNotExist:
        raise Http404
    authuser_trackers = AuthUserTrackerClick.objects.filter(
        destination = tracker
    )
    contact_trackers = ContactTrackerClick.objects.filter(
        destination = tracker
    )
    context = {
        'tracker': tracker,
        'authuser_trackers': authuser_trackers,
        'contact_trackers': contact_trackers,
    }
    return render(request, 'whyness_crm/tracker_item.html', context)

def goto(request, link, user):
    """Send a message via email to a user"""
    msg = "Tracking link: {} : {}".format(link, user)
    logger.debug(msg)

    goto_link = None
    tracked_user = None
    user_type = None
    try:
        goto_link = TrackerDestination.objects.get(xref=link)
    except TrackerDestination.DoesNotExist:
        raise Http404

    msg = "Tracking link goto: {}:{}".format(goto_link, goto_link.url)
    logger.debug(msg)

    try:
        tracked_user = AuthUser.objects.get(xref=user)
        user_type = CONTACT_USER
    except AuthUser.DoesNotExist:
        pass

    if not tracked_user:
        try:
            tracked_user = Contact.objects.get(xref=user)
            user_type = CONTACT_PROSPECT
        except Contact.DoesNotExist:
            # Neither prospect nor registered user
            raise Http404

    msg = "Tracking user: {}:{}".format(user_type, tracked_user)
    logger.debug(msg)

    # Track activity
    (remote_addr, remote_host) = get_host_info(request)
    msg = "Addr/Host: {}:{}".format(remote_addr, remote_host)
    logger.debug(msg)
    try:
        if user_type == CONTACT_USER:
            tracker = AuthUserTrackerClick(
                destination=goto_link,
                contact=tracked_user,
                update_ip=remote_addr,
            )
            tracker.save()
            mpe = Event()
            mpe.event = "User click"
            mpe.insert_id = tracker.id
            mpe.time = int(tracker.create_date.timestamp())
            if tracker.contact.id == 1:
                mpe.user = ""
            else:
                mpe.user = tracker.contact.id
            mpe.ip = tracker.update_ip
            mpe.data = "{}: {}".format(tracker.destination.xref, tracker.destination.title)
            mpe.send()
        elif user_type == CONTACT_PROSPECT:
            tracker = ContactTrackerClick(
                destination=goto_link,
                contact=tracked_user,
                update_ip=remote_addr,
            )
            tracker.save()

            mpe = Event()
            mpe.event = "Prospect click"
            mpe.insert_id = tracker.id
            mpe.time = int(tracker.create_date.timestamp())
            if tracker.contact.id == 1:
                mpe.user = ""
            else:
                mpe.user = "p:{}".format(tracker.contact.id)
            mpe.ip = tracker.update_ip
            mpe.data = "{}: {}".format(tracker.destination.xref, tracker.destination.title)
            mpe.send()
        else:
            msg = "Not saving tracking event: {} {}:".format(
                link,
                user,
                err,
            )
            logger.error(msg)
    except Exception as err:
        msg = "Could not save tracking event: {} for: {}:".format(
            link,
            user,
            err,
        )
        logger.error(msg)

    return HttpResponseRedirect(goto_link.url)

def user_status(request):
    """Show all names of users and email and each questionnaire and date

    red if users have not completed questionnaires
    green if users have completed each time"""
    if not request.user.is_verified:
        return HttpResponseRedirect(reverse('home'))
    custom_result = None
    custom_columns = None

    raw_sql = """SELECT c.name, c.email,
    MIN(dj.create_date) AS dj_date,
    MIN(ss.create_date) AS ss_date,
    MIN(story.create_date) AS story_date
    FROM whyness_django_authuser AS c
    LEFT OUTER JOIN whyness_appgyver_polls_dreamjob AS dj
    ON c.id = dj.user_id
    LEFT OUTER JOIN whyness_appgyver_polls_sweetspot AS ss
    ON c.id = ss.user_id
    LEFT OUTER JOIN whyness_django_audio AS story
    ON c.id = story.user_id
    GROUP BY c.name, c.email
    ORDER BY c.name, c.email
"""

    # Fetch custom result
    with connection.cursor() as cursor:
        cursor.execute(raw_sql)
        custom_columns = [col[0] for col in cursor.description]
        custom_result = cursor.fetchall()

    context = {
        'custom_columns': custom_columns,
        'custom_result': custom_result,
    }
    return render(request, 'whyness_crm/user_status.html', context)

def user_stories(request):
    """Show all names of users and email and number of stories recorded and date

    red if users has recorded less than 3 new stories
    green if users has recorded more than 3 new stories
    Show when new stories/recordings are complete by user

    Show all names of users and email and number of transcripts and how many transcripts read and date

    red if users have NOT read their transcripts at least two transcript
    green if users have read their transcripts"""
    if not request.user.is_verified:
        return HttpResponseRedirect(reverse('home'))
    limit = 100
    custom_result = None
    custom_columns = None

    raw_sql = """SELECT c.name, c.email,
    (SELECT count(id)
    FROM whyness_django_audio AS s
    WHERE c.id = s.user_id) as count,
    (SELECT max(create_date)
    FROM whyness_django_audio AS s
    WHERE c.id = s.user_id) as max_data
    FROM whyness_django_authuser AS c
    ORDER BY c.name, c.email
    """

    # Fetch custom result
    with connection.cursor() as cursor:
        cursor.execute(raw_sql)
        custom_columns = [col[0] for col in cursor.description]
        custom_result = cursor.fetchall()

    context = {
        'limit': limit,
        'custom_columns': custom_columns,
        'custom_result': custom_result,
    }
    return render(request, 'whyness_crm/user_stories.html', context)

def user_stories_week(request):
    """Show all users and email and number of stories recorded per week
    isoyear is used as ISO 8601 weeks can start in December
    """
    if not request.user.is_verified:
        return HttpResponseRedirect(reverse('home'))
    custom_result = None
    custom_columns = None

    raw_sql = """
        SELECT
            c.name, c.email,
            EXTRACT(isoyear FROM s.create_date) AS year,
            EXTRACT(week FROM s.create_date) AS week,
            count(*)
        FROM whyness_django_authuser AS c
        INNER JOIN whyness_django_audio AS s
        ON c.id = s.user_id
        GROUP BY 1, 2, 3, 4
        ORDER BY 1, 2, 3, 4
    """

    # Fetch custom result
    with connection.cursor() as cursor:
        cursor.execute(raw_sql)
        custom_columns = [col[0] for col in cursor.description]
        custom_result = cursor.fetchall()

    context = {
        'custom_columns': custom_columns,
        'custom_result': custom_result,
    }
    return render(request, 'whyness_crm/user_stories_week.html', context)

def user_transcript_readers_week(request):
    """Weekly number of users who have read their own transcripts
    """
    if not request.user.is_verified:
        return HttpResponseRedirect(reverse('home'))
    custom_result = None
    custom_columns = None

    raw_sql = """
SELECT
    count("week-4") AS "week-4",
    count("week-3") AS "week-3",
    count("week-2") AS "week-2",
    count("week-1") AS "week-1"
FROM (
SELECT c.email,
(SELECT DISTINCT story.user_id AS "week-4"
FROM whyness_django_audio AS story

INNER JOIN whyness_django_trackerlog AS log
ON story.update_date < log.create_date
AND log.method='GET'
AND log.user_id = c.id
AND EXTRACT(isoyear FROM log.create_date) = EXTRACT(isoyear FROM now() - interval '4 week')
AND EXTRACT(week FROM log.create_date) = EXTRACT(week FROM now() - interval '4 week')

INNER JOIN whyness_django_trackeritem AS item
ON log.item_id = item.id
AND item.title = 'media'
WHERE story.status = 8
AND story.user_id = c.id
),
(SELECT DISTINCT story.user_id AS "week-3"
FROM whyness_django_audio AS story

INNER JOIN whyness_django_trackerlog AS log
ON story.update_date < log.create_date
AND log.method='GET'
AND log.user_id = c.id
AND EXTRACT(isoyear FROM log.create_date) = EXTRACT(isoyear FROM now() - interval '3 week')
AND EXTRACT(week FROM log.create_date) = EXTRACT(week FROM now() - interval '3 week')

INNER JOIN whyness_django_trackeritem AS item
ON log.item_id = item.id
AND item.title = 'media'
WHERE story.status = 8
AND story.user_id = c.id
),
(SELECT DISTINCT story.user_id AS "week-2"
FROM whyness_django_audio AS story

INNER JOIN whyness_django_trackerlog AS log
ON story.update_date < log.create_date
AND log.method='GET'
AND log.user_id = c.id
AND EXTRACT(isoyear FROM log.create_date) = EXTRACT(isoyear FROM now() - interval '2 week')
AND EXTRACT(week FROM log.create_date) = EXTRACT(week FROM now() - interval '2 week')

INNER JOIN whyness_django_trackeritem AS item
ON log.item_id = item.id
AND item.title = 'media'
WHERE story.status = 8
AND story.user_id = c.id
),
(SELECT DISTINCT story.user_id AS "week-1"
FROM whyness_django_audio AS story

INNER JOIN whyness_django_trackerlog AS log
ON story.update_date < log.create_date
AND log.method='GET'
AND log.user_id = c.id
AND EXTRACT(isoyear FROM log.create_date) = EXTRACT(isoyear FROM now() - interval '1 week')
AND EXTRACT(week FROM log.create_date) = EXTRACT(week FROM now() - interval '1 week')

INNER JOIN whyness_django_trackeritem AS item
ON log.item_id = item.id
AND item.title = 'media'
WHERE story.status = 8
AND story.user_id = c.id
)

FROM whyness_django_authuser AS c
) AS readers

    """

    # Fetch custom result
    with connection.cursor() as cursor:
        cursor.execute(raw_sql)
        custom_columns = [col[0] for col in cursor.description]
        custom_result = cursor.fetchall()

    context = {
        'custom_columns': custom_columns,
        'custom_result': custom_result,
    }
    return render(request, 'whyness_crm/user_transcript_readers_week.html', context)

def user_ai(request):
    """Show all name and email of users that has a new AI analysis

    red if user has no AI analysis
    green if user has AI analysis"""
    if not request.user.is_verified:
        return HttpResponseRedirect(reverse('home'))
    limit = 100
    custom_result = None
    custom_columns = None

    raw_sql = """SELECT c.name, c.email,
    (SELECT count(id)
    FROM whyness_django_audio AS s
    WHERE c.id = s.user_id) as count,
    (SELECT max(create_date)
    FROM whyness_django_audio AS s
    WHERE c.id = s.user_id) as max_data
    FROM whyness_django_authuser AS c
    ORDER BY c.name, c.email
    """

    # Fetch custom result
    #with connection.cursor() as cursor:
    #    cursor.execute(raw_sql)
    #    custom_columns = [col[0] for col in cursor.description]
    #    custom_result = cursor.fetchall()

    context = {
        'limit': limit,
        'custom_columns': custom_columns,
        'custom_result': custom_result,
    }
    return render(request, 'whyness_crm/user_ai.html', context)

def app_aggregate(request):
    """Various app summary reports"""
    if not request.user.is_verified:
        return HttpResponseRedirect(reverse('home'))
    custom_result = None
    custom_columns = None

    raw_sql = """SELECT title, count_of
FROM (
SELECT 'Total users' AS title, count(*) as count_of, 1 AS sort_order
FROM whyness_django_authuser
UNION
SELECT 'Dream Job' AS title, count(*) as count_of, 2 AS sort_order
FROM (
    SELECT user_id
    FROM whyness_appgyver_polls_dreamjob
    GROUP BY user_id
) AS dj
UNION
SELECT 'Sweet Spot' AS title, count(*) as count_of, 3 AS sort_order
FROM (
    SELECT user_id
    FROM whyness_appgyver_polls_sweetspot
    GROUP BY user_id
) AS ss
UNION
SELECT 'AI analysis' AS title, count(*) as count_of, 4 AS sort_order
FROM (
    SELECT user_id
    FROM whyness_django_audio
    WHERE status = 8
    GROUP BY user_id
) AS aianalysis
UNION
SELECT 'AI review' AS title, count(*) as count_of, 5 AS sort_order
FROM (
    SELECT story.user_id
    FROM whyness_django_audio AS story
    INNER JOIN whyness_django_trackerlog AS log
    ON story.update_date >= log.create_date
    AND log.method='GET'
    INNER JOIN whyness_django_trackeritem AS item
    ON log.item_id = item.id
    AND item.title = 'media'
    WHERE story.status = 8
) AS aireview
) AS report
ORDER BY sort_order
    """

    # Fetch custom result
    with connection.cursor() as cursor:
        cursor.execute(raw_sql)
        custom_columns = [col[0] for col in cursor.description]
        custom_result = cursor.fetchall()

    context = {
        'custom_columns': custom_columns,
        'custom_result': custom_result,
    }
    return render(request, 'whyness_crm/app_aggregate.html', context)
