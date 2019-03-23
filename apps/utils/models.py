import random
from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField


class ProjectBaseMixin(models.Model):
    """Base mixin model."""

    created = models.DateTimeField(default=timezone.now, editable=False,
                                   verbose_name=_('Date created'))
    modified = models.DateTimeField(auto_now=True,
                                    verbose_name=_('Date updated'))

    class Meta:
        abstract = True


def generate_code():
    """Generate code method."""
    return '%06d' % random.randint(0, 999999)


def image_path(instance, filename):
    """Determine avatar path method."""
    filename = '%s.jpeg' % generate_code()
    return 'image/%s/%s/%s' % (
        instance._meta.model_name,
        datetime.now().strftime(settings.REST_DATE_FORMAT),
        filename)


class ImageMixin(models.Model):
    """Avatar model."""

    THUMBNAIL_KEY = 'default'

    image = ThumbnailerImageField(upload_to=image_path,
                                  blank=True, null=True, default=None,
                                  verbose_name=_('Image'))

    class Meta:
        """Meta class."""

        abstract = True

    def get_image(self, key=None):
        """Get thumbnailed image file."""
        return self.image[key or self.THUMBNAIL_KEY] if self.image else None

    def get_image_url(self, key=None):
        """Get image thumbnail url."""
        return self.get_image(key).url if self.image else None

    def image_tag(self):
        """Admin preview tag."""
        if self.image:
            return mark_safe('<img src="%s" />' % self.get_image_url())
        else:
            return None

    image_tag.short_description = _('Image')
    image_tag.allow_tags = True
