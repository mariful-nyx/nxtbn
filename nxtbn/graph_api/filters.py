import django_filters as filters
from nxtbn.product.models import Category, Collection, Product, Supplier


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    summary = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    category = filters.ModelChoiceFilter(field_name='category', queryset=Category.objects.all())
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    supplier = filters.ModelChoiceFilter(field_name='supplier', queryset=Supplier.objects.all())
    brand = filters.CharFilter(lookup_expr='icontains')
    type = filters.CharFilter(field_name='type', lookup_expr='exact')
    related_to = filters.CharFilter(field_name='related_to__name', lookup_expr='icontains')
    collection = filters.ModelChoiceFilter(field_name='collections', queryset=Collection.objects.all())

    class Meta:
        model = Product
        fields = ('name', 'summary', 'description', 'category', 'category_name', 'supplier', 'brand', 'type', 'related_to', 'collection')