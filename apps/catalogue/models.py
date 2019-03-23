from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from utils.models import ProjectBaseMixin, image_path


class ProductImageManager(models.Manager):
    """Product image manager."""


class ProductImageQuerySet(models.QuerySet):
    """Product image QuerySet."""

    def get_without_vector(self):
        return self.filter(vector_isnull=True)


class ProductImage(ProjectBaseMixin):
    """Product image model."""
    article = models.CharField(verbose_name=_('Article'), max_length=512, unique=True)
    image = models.ImageField(verbose_name=_('Image'), upload_to=image_path)
    vector = models.TextField(verbose_name=_('Vector'), blank=True, null=True, default=None)

    class Meta:
        verbose_name_plural = _('Product images')
        verbose_name = _('Product image')

    def __str__(self):
        return self.article

    def make_vector(self):
        pass

    def get_image(self, key=None):
        """Get image file."""
        return self.image if self.image else None

    def get_image_url(self, key=None):
        """Get image thumbnail url."""
        return self.get_image(key).url if self.image else None

    def image_tag(self):
        """Admin preview tag."""
        if self.image:
            return mark_safe('<img src="%s" width="150" height="150"/>' % self.get_image_url())
        else:
            return None

    image_tag.short_description = _('Image')
    image_tag.allow_tags = True
