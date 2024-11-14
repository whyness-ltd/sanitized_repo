#----------------------------------------------------------------------
# Whyness Mixpanel models
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

"""Mainly Virtual models for working with Mixpanel
Currently implemented as event => mixpanel event
When volume increases, batch events to increase throughput

All posted events might have errors so these must be recorded for debugging.

When batching events:
  Read the last event id sent to mixpanel
  Read a few records (max 2000) after the last event id
  Send the request
  Record the response
  Record the last event id sent to mixpanel
  If the status is 400 bad request, then identify failures and re-submit manually
"""
import json
import logging
import requests
from requests.auth import HTTPBasicAuth

from django.conf import settings
from django.db import models

from whyness_django.models import TrackerLog
from whyness_django.models import UserAgent

logger = logging.getLogger(__name__)

class Log(models.Model):
    """Activity log for all events"""
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    status_code = models.PositiveSmallIntegerField('Status code', default=0)
    message = models.TextField(default="")

class Event(models.Model):
    """Virtual model to send an activity event to Mixpanel
    High-level requirements

    Each event must be properly formatted JSON.
    Each event must contain an event name, time, distinct_id, and $insert_id. These are used to deduplicate events, so that this endpoint can be safely retried.
    Each event must be smaller than 1MB of uncompressed JSON.
    Each event must have fewer than 255 properties.
    All nested object properties must have fewer than 255 keys and max nesting depth is 3.
    All array properties must have fewer than 255 elements.

    distinct_id identifies the user who performed the event. distinct_id must be specified on every event, as it is crucial for Mixpanel to perform behavioral analysis (unique users, funnels, retention, cohorts) correctly and efficiently.

    If the event is not associated with any user, set distinct_id to the empty string. Events with an empty distinct_id will be excluded from all behavioral analysis.
    # https://REMOVED

    Send data as quickly as possible with concurrent clients until the server returns 429. We see the best results with 10-20 concurrent clients sending 2K events per batch.
    When you see 429s, employ an exponential backoff with jitter strategy. We recommend starting with a backoff of 2s and doubling backoff until 60s, with 1-5s of jitter.

    $insert_id is required on all events. This makes it safe to retry /import requests. If your events don't already have a unique ID (eg: a UUID/GUID), we recommend computing a hash of some set of properties that make the event semantically unique (eg: distinct_id + timestamp + some other property) and using the first 36 characters of that hash as the $insert_id.

    Status codes:
    200 ok
    400 some records failed validation
    401 invalid credentials
    413 payload is too large
    429 rate limit exceeded
    """
    id = models.AutoField(primary_key=True)
    # $insert_id provides a unique identifier for the event,
    # which we use for deduplication
    insert_id = models.CharField(max_length=36, default="")
    # This is the name of the event
    event = models.CharField(max_length=100, default="")
    # distinct_id identifies the user who performed the event
    user = models.CharField(max_length=36, default="")
    ip = models.GenericIPAddressField(default='::1')
    useragent = models.CharField(max_length=500, default="")
    data = models.CharField(max_length=250, default="")
    # The time at which the event occurred,
    # in seconds or milliseconds since epoch
    time = models.PositiveIntegerField()

    def __str__(self):
        ret = "{} {} {}".format(self.event, self.time, self.insert_id)
        return ret
    def str(self):
        if not self.insert_id:
            logger.warning("Empty insert_id")
            return ""
        if not self.event:
            logger.warning("Empty event")
            return ""
        if not self.time:
            logger.warning("Empty time")
            return ""
        mp_event = """{{
            "event": "{}",
            "properties": {{
                "distinct_id": "{}",
                "$insert_id": "{}",
                "time": {},
                "useragent": "{}",
                "ip": "{}",
                "data": "{}"
            }}
        }}""".format(
            self.event,
            self.user,
            self.insert_id,
            self.time,
            self.useragent,
            self.ip,
            self.data,
        )
        return str(mp_event)
    def json(self):
        return json.loads(self.str())
    def send(self):
        """Send an event to Mixpanel
        Returns True if some or all events have been sent
        Returns False if 401, 412 or 429 have been returned
        """
        msg = "Sending the following event {}".format(self.json())
        logger.debug(msg)
        basic = HTTPBasicAuth(
            settings.MIXPANEL_SERVICE_ACCOUNT,
            settings.MIXPANEL_SERVICE_PASSWORD
        )
        url_t = "https://REMOVED
        url = url_t.format(settings.MIXPANEL_PROJECT_ID)
        headers = {
            "Accept": "application/x-ndjson",
            "Content-Type": "application/x-ndjson"
        }
        response = requests.post(
            url,
            json=self.json(),
            headers=headers,
            auth=basic,
        )

        logger.debug(response.text)
        ml = Log()
        ml.status_code = response.status_code
        ml.message = response.text
        ml.save()

        ret = False
        if response.status_code == 200:
            #200 ok
            ret = True
        elif response.status_code == 400:
            #400 some records failed validation
            ret = True
        else:
            #401 invalid credentials
            #413 payload is too large
            #429 rate limit exceeded
            ret = False
        return ret

    class Meta:
        managed = False
