from unicodedata import category
import django_filters
from .models import *
class productFilter(django_filters.FilterSet):
    class Meta:
        model = product
        fields = ['category']
        
