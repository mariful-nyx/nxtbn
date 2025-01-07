import django_filters
from nxtbn.product.models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],  # Filter by name using case-insensitive containment
            'brand': ['icontains'],  # Filter by brand
            # 'category__name': ['exact'],  # Filter by exact category name
        }
