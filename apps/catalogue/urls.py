from django.urls import path
from catalogue import views

app_name = 'catalogue'
urlpatterns = [
    path('image/', views.ImageListView.as_view(), name='images_list'),
]