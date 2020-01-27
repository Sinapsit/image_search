"""Vectorization all images."""

from django.core.management.base import BaseCommand
from catalogue.models import ProductImage
from learning.vectorize_hdf5 import Vectorization


class Command(BaseCommand):
    help = 'Vectorization all images.'

    def handle(self, *args, **options):
        qs = ProductImage.objects.available()
        # if options['max']:
        qs = qs.filter(id__in=qs[:600])

        v = Vectorization(qs)
        v.execute()


