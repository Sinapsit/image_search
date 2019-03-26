"""Vectorization all images."""

from django.core.management.base import BaseCommand
from catalogue.models import ProductImage
from learning.vectorize_image import Vectorization


class Command(BaseCommand):
    help = 'Vectorization all images.'

    def handle(self, *args, **options):
        qs = ProductImage.objects.available()
        # if options['max']:
        qs = ProductImage.objects.filter(id__in=qs[:10000])

        v = Vectorization(qs)
        v.execute()


