"""Import images from CSV."""
import argparse
import sys

import pandas as pd
from django.core.management.base import BaseCommand

from catalogue.models import ProductImage, Category
from tqdm import tqdm


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
        df.columns = ['im_name', 'im_url', 'category']
        ProductImage.objects.bulk_create(
            ProductImage(
                category=Category.objects.get_or_create(name=vals['category'])[0],
                article=vals['im_name'],
                external_url=vals['im_url']
            ) for vals in tqdm(df.to_dict('records'), desc='Export image data.')
        )
