#----------------------------------------------------------------------
# Whyness ml models download nltk modules
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
# Download data files for a docker image reducing container spin up time
#----------------------------------------------------------------------

import nltk
import boto3

from os.path import abspath

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'Queue runner'

    def add_arguments(self, parser):
        parser.add_argument(
            '--nltk',
            action='store_true',
            help="nltk modules",
        )
        parser.add_argument(
            '--mbti',
            action='store_true',
            help="mbti pickles",
        )

    def handle(self, *args, **options):
        if options['nltk']:
            base_dir = settings.BASE_DIR
            download_dir = abspath("{}/nltk_data/".format(base_dir))
            msg = "Downloading nltk modules to: {}".format(download_dir)
            self.stdout.write(msg)
            nltk.download('genesis', download_dir)
            nltk.download('gutenberg', download_dir)
            nltk.download('inaugural', download_dir)
            nltk.download('nps_chat', download_dir)
            nltk.download('omw-1.4', download_dir)
            nltk.download('punkt', download_dir)
            nltk.download('stopwords', download_dir)
            nltk.download('treebank', download_dir)
            nltk.download('webtext', download_dir)
            nltk.download('wordnet', download_dir)

        if options['mbti']:
            base_dir = settings.BASE_DIR
            download_dir = abspath("{}/mbti_data/".format(base_dir))
            msg = "Downloading nltk modules to: {}".format(download_dir)
            self.stdout.write(msg)
            # Download latest MBTI data
            s3 = boto3.resource('s3', region_name=settings.AWS_REGION_NAME)
            bucket = s3.Bucket('whyness-ml')

            pickles = [
                'FT.pickle',
                'IE.pickle',
                'JP.pickle',
                'NS.pickle',
                'pretrain_cnt.pickle',
                'pretrain_tfidf.pickle',
            ]

            for pickle in pickles:
                msg = "Downloading: {}".format(pickle)
                self.stdout.write(msg)
                object = bucket.Object(pickle)
                download_file = "{}/{}".format(download_dir, pickle)
                with open(download_file, 'wb') as f:
                    object.download_fileobj(f)

