from django.contrib import admin
from solo.admin import SingletonModelAdmin
from configuration import models


@admin.register(models.LearningConfig)
class LearningConfigAdmin(SingletonModelAdmin):
    """Learning config."""


@admin.register(models.LearningConfigHDF5)
class LearningConfigHDF5Admin(SingletonModelAdmin):
    """Learning HDF5 config."""


@admin.register(models.SuperIndex)
class SuperIndexAdmin(admin.ModelAdmin):
    """Super index admin."""
    list_display = ('id', 'super_category', 'created', 'modified', )
