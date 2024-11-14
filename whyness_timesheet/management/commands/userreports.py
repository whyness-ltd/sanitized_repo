#----------------------------------------------------------------------
# Whyness timesheet reports
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

import datetime
import calendar
import logging

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template import Context, Template
from whyness_timesheet.models import Timeentry

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sends user reports'

    def add_arguments(self, parser):
        parser.add_argument(
            '--list-users',
            action='store_true',
            help="List users",
        )
        parser.add_argument(
            '--timesheet-report',
            action='store_true',
            help="Timesheet report",
        )
        parser.add_argument(
            '--user',
            nargs='?',
            type=str,
            help="User",
        )
        #parser.add_argument('user_id', nargs='+', type=int)

    def handle(self, *args, **options):
        if options['list_users']:
            users = User.objects.all()
            msg = 'Users:'
            self.stdout.write(msg)
            for user in users:
                msg = '{}'.format(user)
                self.stdout.write(msg)
        if options['timesheet_report']:
            try:
                user = User.objects.get(username=options['user'])
                msg = "User {}".format(user.email)
                logger.debug(msg)
            except User.DoesNotExist:
                msg = "User {} does not exist".format(options['user'])
                raise CommandError(msg)

            date_now = datetime.date.today()
            date_start = datetime.date(date_now.year, date_now.month, 1)
            date_end = datetime.date(
                date_now.year,
                date_now.month,
                calendar.monthrange(date_now.year, date_now.month)[-1]
            )
            msg = "Start {} - End {}".format(date_start, date_end)
            logger.debug(msg)

            context = {}

            date_range = calendar.monthrange(date_now.year, date_now.month)
            date_day = date_range[0]
            dt = datetime.date(date_now.year, date_now.month, date_day)
            report = []
            while date_day <= date_range[-1]:
                dt = datetime.date(date_now.year, date_now.month, date_day)
                if dt.weekday() < 5:
                    ts = Timeentry.objects.filter(
                        user=user,
                        date=dt,
                    )
                    if ts:
                        is_okay = ""
                        if ts[0].total() != '7.50':
                            is_okay = " << Please check"

                        msg = "{}: {}{}".format(
                            dt.strftime('%a %d/%m/%Y'),
                            ts[0].total(),
                            is_okay,
                        )
                    else:
                        msg = "{}: {}".format(
                            dt.strftime('%a %d/%m/%Y'),
                            'TODO'
                        )
                if dt.weekday() == 5:
                    msg = '-'
                if dt.weekday() < 6:
                    report.append(msg)
                    self.stdout.write(msg)
                date_day = date_day + 1
            context = {
                'user': user,
                'report': report,
            }
            tpl_txt = """
            Hello {{ user.first_name }},
            Please find your timesheet progress for this month as follows:
            {% for line in report %}
            {{ line }}
            {% endfor %}
            """
            tpl_html = """
            <p>Hello {{ user.first_name }},</p>
            <p>Please find your timesheet progress as follows:</p>
            <p>{% for line in report %}
            {{ line }}</br>
            {% endfor %}</p>
            <p>Many thanks,</p>
            <p>Alan,</p>
            """
            #template = Template(tpl)
            context = Context(context)
            template = Template(tpl_txt)
            msg_text = template.render(context)
            template = Template(tpl_html)
            msg_html = template.render(context)
            subject = "Timesheet report"
            from_email = "email@REMOVED"
            to_email = user.email
            msg = EmailMultiAlternatives(subject, msg_text, from_email, [to_email])
            msg.attach_alternative(msg_html, 'text/html')
            msg.send()
            msg = "Message sent to: {} {}".format(user.first_name, user.last_name)
            self.stdout.write(msg)

