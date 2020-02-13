from django import forms
from activity.models import SearchRequest


class SearchRequestForm(forms.ModelForm):
    class Meta:
        model = SearchRequest
        fields = ['image']
