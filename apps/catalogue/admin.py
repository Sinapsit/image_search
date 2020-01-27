from django.contrib import admin
from catalogue import models
from django.utils.translation import ugettext_lazy as _


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin."""


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'created', 'image_tag', 'status',
                    'category',  'is_vectorized', ]
    search_fields = ['article']
    readonly_fields = ('id', 'created', 'modified', 'image_tag', 'status')
    list_filter = ('status', 'category')
    fieldsets = (
        (_('Info'), {
            'fields': (
                'id', 'created', 'modified',
            )
        }
         ),
        (_('Trade info'), {
            'fields': (
                'article', 'category'
            )
        }
         ),
        (_('Files'), {
            'fields': (
                'image', 'image_tag', 'status'
            )
        }
         ),
        (_('Machine learning'), {
            'fields': (
                'is_vectorized',
            )
        }
         ),
    )
