"""Partner filters."""
from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as filters

from catalogue import models


class ImageListFilter(filters.FilterSet):
    article = filters.CharFilter(
        label=_('Article'),
    )

    class Meta:
        model = models.ProductImage
        fields = (
            'article',
        )
