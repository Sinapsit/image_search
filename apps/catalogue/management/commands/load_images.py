"""Load images from remote server."""

from django.core.management.base import BaseCommand

from catalogue.models import ProductImage
import concurrent.futures
import requests
import threading
import time
thread_local = threading.local()


class Command(BaseCommand):
    help = 'Load images from remote server.'

    def handle(self, *args, **options):
        for i in range(100):
            print(f"Attempt number: {i + 1}")
            try:
                img = ProductImage.objects.load_images()
                print(f"Total: {img.count()} was loaded.")
                break
            except Exception as er:
                print(f"Error{er}")

    # def get_session(self):
    #     if not getattr(thread_local, "session", None):
    #         thread_local.session = requests.Session()
    #     return thread_local.session
    #
    # def download_site(self, url):
    #     session = self.get_session()
    #     with session.get(url) as response:
    #         print(f"Read {len(response.content)} from {url}")
    #
    # def download_all_sites(self, sites):
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    #         executor.map(self.download_site, sites)
    #
    # def handle_2(self, *args, **options):
    #     pass









