from rest_framework import generics, status
from rest_framework.response import Response

from catalogue import serializers, models, filters
from learning.predict import Predict
from learning.predict_old import Predict as OldPredict
from django.views.generic import ListView, CreateView
from django.http import HttpResponseRedirect
from .models import ProductImage
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render
import os
from activity.models import SearchRequest
from catalogue.forms import SearchRequestForm


class PhotoUploadView(CreateView):
    model = SearchRequest
    form_class = SearchRequestForm
    template_name = 'catalogue/base.html'
    success_url = '/catalogue/results/'

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.save()
        instance = form.instance
        pred = OldPredict(search_instance=instance)
        similar = pred.similarity()
        category = pred.category
        search_products = instance.save_result(similar)
        return render(self.request, 'catalogue/results.html', {
            'search_products': search_products,
            'category': category,
            'search_instance': instance
        })


class SearchResultsView(ListView):
    model = ProductImage
    template_name = 'catalogue/results.html'


class ImageListView(generics.ListAPIView):
    """Image list view."""
    serializer_class = serializers.ImageSerializer
    queryset = models.ProductImage.objects.all()
    filter_class = filters.ImageListFilter
    # filter_backends = (DjangoFilterBackend,)


class ImageSearchView(generics.GenericAPIView):
    """Search image by image view."""
    serializer_class = serializers.ImageSearchSerializer
    queryset = models.ProductImage.objects.all()

    def post(self, request, *args, **kwargs):
        """Delete method."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = request.data['image']
        # save tamp file
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image.name)
        path = default_storage.save(save_path, image)
        # path = 'media/media/image/productimage/03-24-2019/000205.jpeg'
        pred = Predict(path=path, list_content='article')
        similar = pred.similarity()

        list_data = [i[0] for i in similar]
        qs = self.queryset.filter(article__in=list_data)
        images = serializers.ImageSerializer(qs, many=True).data
        return Response(data=images, status=status.HTTP_200_OK)
