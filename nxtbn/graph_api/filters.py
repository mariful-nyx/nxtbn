import django_filters
from nxtbn.product.models import Product

class ProductFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")

    class Meta:
        model = Product
        fields = ["status"]