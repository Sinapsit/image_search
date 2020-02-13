from django.db import models
from solo.models import SingletonModel
from django.contrib.postgres.fields import ArrayField
# Create your models here.
from utils.models import vector_path
from django.utils.translation import ugettext_lazy as _
from utils.models import ProjectBaseMixin


class LearningConfig(SingletonModel):
    file = models.FileField(_('File'), upload_to=vector_path)
    filename_list = ArrayField(models.CharField(max_length=512),
                               verbose_name=_('Filename list'),
                               null=True, default=None)
    article_list = ArrayField(models.CharField(max_length=512),
                              verbose_name=_('Article list'),
                              null=True, default=None)


class LearningConfigHDF5(SingletonModel):
    file = models.FileField(_('File'), upload_to=vector_path)
    filename_list = ArrayField(models.CharField(max_length=512),
                               verbose_name=_('Filename list'),
                               null=True, default=None)
    article_list = ArrayField(models.CharField(max_length=512),
                              verbose_name=_('Article list'),
                              null=True, default=None)


class SuperIndexManager(models.Manager):
    """SuperIndex manager."""


class SuperIndexQuerySet(models.QuerySet):
    """SuperCategoryIndex QuerySet."""


class SuperIndex(ProjectBaseMixin):
    """Super index model."""
    super_category = models.CharField(_('Super category'), max_length=255)
    vectors = models.FileField(_('Vectors'), upload_to=vector_path)
    filename_list = ArrayField(models.CharField(max_length=512),
                               verbose_name=_('Filename list'),
                               null=True, default=None)
    article_list = ArrayField(models.CharField(max_length=512),
                              verbose_name=_('Article list'),
                              null=True, default=None)

    objects = SuperIndexManager.from_queryset(SuperIndexQuerySet)()
