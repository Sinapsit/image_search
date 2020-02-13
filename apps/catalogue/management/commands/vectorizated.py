"""Vectorization all images."""

from django.core.management.base import BaseCommand
from catalogue.models import ProductImage, Category
from learning.vectorize_image import Vectorization


class Command(BaseCommand):
    help = 'Vectorization all images.'

    def add_arguments(self, parser):
        parser.add_argument('category', nargs='+', type=str)

    def handle(self, *args, **options):
        qs = ProductImage.objects.available()
        super_categories = dict(Category.SUPER_CATEGORY_CHOICES)
        for key, value in super_categories.items():
            if options['category'] and key not in options['category']:
                continue
            self.stdout.write(
                self.style.SUCCESS(f'Vectorization category "{value}"\n'))
            v = Vectorization(qs, key)
            v.execute()


