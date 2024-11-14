#----------------------------------------------------------------------
# Whyness CRM import
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

import logging
import csv

from django.core.management.base import BaseCommand, CommandError
from whyness_crm.models import Contact

logger = logging.getLogger(__name__)

STATUS_ACTIVE = 1

class Command(BaseCommand):
    help = 'Import contacts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help="Test import",
        )
        parser.add_argument(
            '--file',
            nargs='?',
            type=str,
            help="File to import",
        )

    def handle(self, *args, **options):
        data = None
        import_file = options['file']
        is_first = True
        with open(import_file, newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            i = 1
            for row in spamreader:
                i=i+1
                if is_first:
                    # Ignore the first title row
                    is_first = False
                    continue
                try:
                    data = Contact.objects.get(email=row[1])
                except Contact.DoesNotExist:
                    if options['test']:
                        msg = "Can insert new record: {}:{}".format(row[0], row[1])
                    else:
                        msg = "Inserting new record: {}:{}".format(row[0], row[1])
                    self.stdout.write(msg)
                    data = Contact(
                        status=STATUS_ACTIVE,
                        is_prospect=True,
                        is_registered=False,
                        use_whatsapp=False,
                        use_email=True,
                        name=row[0],
                        email=row[1],
                    )
                    if not options['test']:
                        data.save()
                        msg = "New prospect saved"
                        self.stdout.write(msg)
