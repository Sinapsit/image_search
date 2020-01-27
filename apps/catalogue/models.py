from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from utils.models import ProjectBaseMixin, image_path
from utils.tools import GetRemoteImage
from tqdm import tqdm


class Category(models.Model):
    """Product category model."""
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return f'{self.name}'


class ProductImageManager(models.Manager):
    """Product image manager."""

    def load_images(self):
        qs = self.filter(status=ProductImage.NOT_LOADED)
        for obj in tqdm(qs):
            obj.load_image()
        return qs


class ProductImageQuerySet(models.QuerySet):
    """Product image QuerySet."""

    def get_without_vector(self):
        return self.filter(vector_isnull=True)

    def available(self):
        return self.filter(status=ProductImage.LOADED)


class ProductImage(ProjectBaseMixin):
    """Product image model."""
    NOT_LOADED = 0
    LOADED = 1
    NOT_FOUND = 3

    STATUS_CHOICES = (
        (NOT_LOADED, _("Not loaded")),
        (LOADED, _('Loaded')),
        (NOT_FOUND, _('Not found'))
    )

    article = models.CharField(verbose_name=_('Article'), max_length=512, unique=True)
    image = models.ImageField(verbose_name=_('Image'), upload_to=image_path)
    external_url = models.URLField(_('External URL'), null=True, default=None)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=NOT_LOADED)
    is_vectorized = models.BooleanField(_('Is vectorized'), default=False)
    category = models.ForeignKey(
        Category, verbose_name='category', null=True,
        default=None, on_delete=models.CASCADE)

    objects = ProductImageManager.from_queryset(ProductImageQuerySet)()

    class Meta:
        verbose_name_plural = _('Product images')
        verbose_name = _('Product image')
        ordering = ('article',)

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
            return mark_safe(
                f'<a href={ self.get_image_url() }>'
                f'<img src="{self.get_image_url() }" width="150" height="150"/>'
                f'</a>')
        else:
            return None

    def load_image(self):
        GetRemoteImage(self).load()

    image_tag.short_description = _('Image')
    image_tag.allow_tags = True
