from rest_framework import generics, status
from rest_framework.response import Response

from catalogue import serializers, models, filters
from utils.tools import SearchByVector


class ImageListView(generics.ListAPIView):
    """Image list view."""
    serializer_class = serializers.ImageSerializer
    queryset = models.ProductImage.objects.all()
    filter_class = filters.ImageListFilter
    # filter_backends = (DjangoFilterBackend,)


class ImageSearchView(generics.GenericAPIView):
    """Search image by image view."""
    serializer_class = serializers.ImageSearchSerializer

    def post(self, request, *args, **kwargs):
        """Delete method."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.data['image']
        qs = SearchByVector(
            image=image
        ).get_similar(
            queryset=models.ProductImage.objects.all()
        )
        images = serializers.ImageSerializer(qs, many=True).data
        return Response(data=images, status=status.HTTP_200_OK)
