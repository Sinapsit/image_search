from django.contrib import admin
from catalogue import models
from django.utils.translation import ugettext_lazy as _


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'created', 'image_tag']
    search_fields = ['articles']
    readonly_fields = ('id', 'created', 'modified', 'image_tag')
    fieldsets = (
        (_('Info'), {
            'fields': (
                'id', 'created', 'modified',
            )
        }
         ),
        (_('Trade info'), {
            'fields': (
                'article',
            )
        }
         ),
        (_('Files'), {
            'fields': (
                'image', 'image_tag'
            )
        }
         ),
        (_('AI_Data'), {
            'fields': (
                'vector',
            )
        }
         ),
    )

