"""Vectorization images."""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Vectorization images.'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        """Vectorization images."""
        if options['delete']:
            print('All data was deleted!!')
