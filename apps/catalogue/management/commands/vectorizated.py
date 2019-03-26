"""Vectorization all images."""

from django.core.management.base import BaseCommand
from catalogue.models import ProductImage
from learning.vectorize_image import Vectorization


class Command(BaseCommand):
    help = 'Vectorization all images.'

    def handle(self, *args, **options):
        qs_slice = ProductImage.objects.available()[:1000]
        qs = ProductImage.objects.filter(id__in=qs_slice)
        v = Vectorization(qs)
        v.execute()


