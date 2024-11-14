#----------------------------------------------------------------------
# Whyness Mixpanel commands
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
# Send any of:
#   Tracker
#   AuthUserTrackerClick
#   ContactTrackerClick
# See model for sending information
#----------------------------------------------------------------------

import datetime
import logging

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from whyness_django.models import TrackerLog

from whyness_crm.models import AuthUserTrackerClick
from whyness_crm.models import ContactTrackerClick

from whyness_mixpanel.models import Log
from whyness_mixpanel.models import Event

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sends events'

    def add_arguments(self, parser):
        parser.add_argument(
            '--activity',
            nargs=1,
            type=int,
            default=0,
            help="Activity",
        )
        parser.add_argument(
            '--user-click',
            nargs=1,
            type=int,
            default=0,
            help="User Click",
        )
        parser.add_argument(
            '--contact-click',
            nargs=1,
            type=int,
            default=0,
            help="Contact Click",
        )
    def handle(self, *args, **options):
        if options['activity']:
            try:
                tracker = TrackerLog.objects.get(id=options['activity'][0])
            except TrackerLog.DoesNotExist:
                msg = "Activity {} does not exist".format(options['activity'])
                raise CommandError(msg)
            # Prepare request
            mpe = Event()
            mpe.event = tracker.item.title
            mpe.insert_id = tracker.id
            mpe.time = int(tracker.create_date.timestamp())
            if tracker.user.id == 1:
                mpe.user = ""
            else:
                mpe.user = tracker.user.id
            mpe.ip = tracker.ip
            mpe.useragent = tracker.useragent.useragent
            mpe.data = tracker.method
            if not mpe.send():
                msg = "Error sending Mixpanel event: {}".format(mpe.insert_id)

        elif options['user_click']:
            """Send user click events to Mixpanel"""
            msg = 'User click:'
            self.stdout.write(msg)
            try:
                tracker = AuthUserTrackerClick.objects.get(id=options['user_click'][0])
            except AuthUserTrackerClick.DoesNotExist:
                msg = "User click {} does not exist".format(options['user_click'])
                raise CommandError(msg)
            # Prepare request
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
            if not mpe.send():
                msg = "Error sending Mixpanel user event: {}".format(mpe.insert_id)
        elif options['contact_click']:
            """Send prospect click events to Mixpanel"""
            msg = 'Contact click:'
            self.stdout.write(msg)
            try:
                tracker = ContactTrackerClick.objects.get(id=options['contact_click'][0])
            except ContactTrackerClick.DoesNotExist:
                msg = "Contact click {} does not exist".format(options['contact_click'])
                raise CommandError(msg)
            # Prepare request
            mpe = Event()
            mpe.event = "Contact click"
            mpe.insert_id = tracker.id
            mpe.time = int(tracker.create_date.timestamp())
            if tracker.contact.id == 1:
                mpe.user = ""
            else:
                mpe.user = "p:{}".format(tracker.contact.id)
            mpe.ip = tracker.update_ip
            mpe.data = "{}: {}".format(tracker.destination.xref, tracker.destination.title)
            if not mpe.send():
                msg = "Error sending Mixpanel user event: {}".format(mpe.insert_id)
        else:
            msg = 'Please supply an tracker, user or contact event to submit:'
            self.stdout.write(msg)
