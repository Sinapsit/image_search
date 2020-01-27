from rest_framework import serializers
from catalogue import models
import os
from django.conf import settings


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = [
            "id",
            "article",
            "external_url",
            "image",
            "category",
        ]


class ImageSearchSerializer(serializers.Serializer):
    """Image Search serializer."""
    image = serializers.ImageField()

    class Meta:
        fields = [
            'image'
        ]

    # def save(self, ):
    #     save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', "image")
    #     return default_storage.save(save_path, image)


