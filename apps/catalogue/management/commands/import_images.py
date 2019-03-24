"""Import images from CSV."""
import argparse
import sys

import pandas as pd
from django.core.management.base import BaseCommand

from catalogue.models import ProductImage


class Command(BaseCommand):
    help = 'Import images from CSV.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            'path', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
            help='the file where the image URL should be read')

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        # ...
        if options['delete']:
            print('All data was deleted!!')
            ProductImage.objects.all().delete()

        csv = options['path']
        df = pd.read_csv(csv)
        df.columns = ['article', 'external_url']
        ProductImage.objects.bulk_create(
            ProductImage(**vals) for vals in df.to_dict('records')
        )
