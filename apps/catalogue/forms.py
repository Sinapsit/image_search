from django import forms
from .models import ProductImage


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
