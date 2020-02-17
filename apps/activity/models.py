from django.db import models
from utils.models import ProjectBaseMixin, ImageMixin
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from catalogue.models import ProductImage


class SearchRequest(ImageMixin, ProjectBaseMixin):
    """Search request model."""
    products = models.ManyToManyField(
        'catalogue.ProductImage', verbose_name=_('products'), through='activity.SearchProduct')

    class Meta:
        verbose_name = _('search request')
        verbose_name_plural = _('search requests')

    def get_similar(self, similar):
        result = [i[0] for i in similar]
        qs = ProductImage.objects.filter(
            article__in=result,
        ).annotate_vector_dist(similar).order_by('vector_dist')
        return qs

    def save_result(self, similar):
        list_data = []
        qs = self.get_similar(similar)
        for product_id, score in qs.values_list('id', 'vector_dist'):
            list_data.append(SearchProduct(
                search_request=self,
                score=score,
                product_id=product_id
            ))
        SearchProduct.objects.bulk_create(list_data)
        return self.search_products.order_by('score')


class SearchProduct(models.Model):
    """Search products model."""
    search_request = models.ForeignKey(
        SearchRequest, verbose_name=_('search request'), related_name='search_products',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        'catalogue.ProductImage', verbose_name=_('product'),
        related_name='search_products', on_delete=models.CASCADE)
    score = models.FloatField()

    class Meta:
        verbose_name = _('search product')
        verbose_name_plural = _('search products')
