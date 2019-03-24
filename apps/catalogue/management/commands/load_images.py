"""Load images from remote server."""

from django.core.management.base import BaseCommand

from catalogue.models import ProductImage


class Command(BaseCommand):
    help = 'Load images from remote server.'

    def handle(self, *args, **options):
        for i in range(10):
            print(f"Attempt number: {i + 1}")
            try:
                img = ProductImage.objects.load_images()
                print(f"Total: {img.count()} was loaded.")
                break
            except Exception as er:
                print(f"Error{er}")


