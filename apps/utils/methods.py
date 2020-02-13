"""Utils mathods"""
import random
from datetime import datetime
from django.conf import settings


def generate_code():
    """Generate code method."""
    return '%06d' % random.randint(0, 999999)


def image_path(instance, filename):
    """Determine image path method."""
    filename = '%s.jpeg' % generate_code()
    return 'image/%s/%s/%s' % (
        instance._meta.model_name,
        datetime.now().strftime(settings.REST_DATE_FORMAT),
        filename)


def file_path(instance, filename):
    """Determine file path method."""
    return 'file/%s/%s/%s' % (
        instance._meta.model_name,
        datetime.now().strftime(settings.REST_DATE_FORMAT),
        filename)