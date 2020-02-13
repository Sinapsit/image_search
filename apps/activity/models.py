from django.db import models
from utils.models import ProjectBaseMixin, ImageMixin
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _


class SearchRequest(ImageMixin, ProjectBaseMixin):
    """Search request model."""
    result = ArrayField(models.CharField(max_length=512), blank=True, default=list)

    class Meta:
        verbose_name = _('search request')
        verbose_name_plural = _('search requests')
