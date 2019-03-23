from rest_framework import generics
from catalogue import serializers, models,filters


class ImageListView(generics.ListAPIView):
    """Image list view."""
    serializer_class = serializers.ImageSerializer
    queryset = models.ProductImage.objects.all()
    filter_class = filters.ImageListFilter
    # filter_backends = (DjangoFilterBackend,)
