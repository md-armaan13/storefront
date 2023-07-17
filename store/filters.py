#import Filterset
from django_filters import FilterSet

# Import models
from .models import Product

# Import filters

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'price': ['gt', 'lt'],
        }