from rest_framework import generics, status
from rest_framework.response import Response

from catalogue import serializers, models, filters
from learning.predict import Predict
from django.views.generic import ListView, CreateView
from django.http import HttpResponseRedirect
from .models import ProductImage
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render
import os


class PhotoUploadView(CreateView):
    model = ProductImage
    fields = ['image']
    template_name = 'catalogue/base.html'  # <app>/<model>_<viewtype>.html
    success_url = '/catalogue/results/'  # /results/ if in url path('results/',...name='something')
    queryset = models.ProductImage.objects.all()

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        image = form.files['image']
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image._name)
        path = default_storage.save(save_path, image)
        pred = Predict(path=path, list_content='article').similarity()
        print(pred)
        list_data = [i[0] for i in pred if i[1] < settings.SEARCH_ACCURACY]
        qs = self.queryset.filter(article__in=list_data).annotate_vector_dist(pred).order_by('vector_dist')
        # images = serializers.ImageSerializer(qs, many=True).data
        return render(self.request, 'catalogue/results.html', {'images': qs,
                                                               'search_img': path.split('/')[-1]})


class SearchResultsView(ListView):
    model = ProductImage
    template_name = 'catalogue/results.html'  # <app>/<model>_<viewtype>.html
    # context_object_name = 'results'


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
        pred = Predict(path=path, list_content='article').similarity()
        list_data = [i[0] for i in pred]
        qs = self.queryset.annotate_vector_dist(pred).filter(article__in=list_data)
        images = serializers.ImageSerializer(qs, many=True).data
        return Response(data=images, status=status.HTTP_200_OK)
