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
