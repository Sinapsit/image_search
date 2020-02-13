from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from tqdm import tqdm

from utils.models import ProjectBaseMixin, image_path, ImageMixin
from utils.tools import GetRemoteImage


class Category(models.Model):
    """Product category model."""
    COMPUTER_CHAIR = 'computer_chair'
    ARMCHAIR_OTTOMAN = 'armchair_ottoman'
    SOFA_BED_CHAIR = 'sofa_bed_chair'
    TABLE = 'table'
    CHAIR = 'chair'  # chair, hard armchair
    CABINET = 'cabinet'  # bedside tables, chest of drawers, cupboard, cabinets
    OTHER = 'other'

    SUPER_CATEGORY_CHOICES = (
        (COMPUTER_CHAIR, _('computer chair')),
        (ARMCHAIR_OTTOMAN, _('armchair ottoman')),
        (SOFA_BED_CHAIR, _('sofa bed chair')),
        (TABLE, _('table')),
        (CHAIR, _('chair')),
        (CABINET, _('cabinet')),
        (OTHER, _('other'))
    )

    name = models.CharField(_("name"), max_length=255)
    super_category = models.CharField(
        _("super category"), choices=SUPER_CATEGORY_CHOICES, max_length=255,
        default=OTHER)

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

    def annotate_vector_dist(self, img_list):
        whens = [
            models.When(article=k, then=v) for k, v in img_list
        ]
        return self.annotate(
            vector_dist=models.Case(
                *whens,
                default=0,
                output_field=models.FloatField()
            )
        )


class ProductImage(ProjectBaseMixin, ImageMixin):
    """Product image model."""
    NOT_LOADED = 0
    LOADED = 1
    NOT_FOUND = 3
    BAD_FORMAT = 4

    STATUS_CHOICES = (
        (NOT_LOADED, _("Not loaded")),
        (LOADED, _('Loaded')),
        (NOT_FOUND, _('Not found')),
        (BAD_FORMAT, _('Bad format')),

    )

    article = models.CharField(verbose_name=_('Article'), max_length=512, unique=True)
    external_url = models.URLField(_('External URL'), null=True, default=None)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=NOT_LOADED)
    is_vectorized = models.BooleanField(_('Is vectorized'), default=False)
    category = models.ForeignKey(
        Category, verbose_name='category', null=True,
        default=None, on_delete=models.CASCADE)

    error = models.TextField(blank=True, null=True, default=None)

    objects = ProductImageManager.from_queryset(ProductImageQuerySet)()

    class Meta:
        verbose_name_plural = _('Product images')
        verbose_name = _('Product image')
        ordering = ('article',)

    def __str__(self):
        return self.article

    def make_vector(self):
        pass

    def load_image(self):
        GetRemoteImage(self).load()
