from rest_framework import serializers
from catalogue import models


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = [
            "id",
            "article",
            "image"
        ]


class ImageSearchSerializer(serializers.Serializer):
    """Image Search serializer."""
    image = serializers.ImageField()

    class Meta:
        fields = [
            'image'
        ]


