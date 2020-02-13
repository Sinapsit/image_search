from django.contrib import admin
from activity import models


@admin.register(models.SearchRequest)
class SearchRequest(admin.ModelAdmin):
    """Search request admin."""
    list_display = ['id', 'created', 'modified', 'image_tag']
