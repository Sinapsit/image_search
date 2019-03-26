from django.urls import path
from catalogue import views

app_name = 'catalogue'
urlpatterns = [
    path('image/', views.ImageListView.as_view(), name='images_list'),
    path('image/search', views.ImageSearchView.as_view(), name='images_search'),

    path('', views.PhotoUploadView.as_view(), name='upload'),
    path('results/', views.SearchResultsView.as_view(), name='results'),
]