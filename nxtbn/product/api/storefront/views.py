from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions  import AllowAny
from rest_framework.exceptions import APIException

from rest_framework import filters as drf_filters
import django_filters
from django_filters import rest_framework as filters


from nxtbn.core.paginator import NxtbnPagination
from nxtbn.product.api.storefront.serializers import CategorySerializer, CollectionSerializer, ProductDetailSerializer, ProductWithDefaultVariantSerializer, ProductWithVariantSerializer, ProductDetailWithRelatedLinkMinimalSerializer
from nxtbn.product.models import Category, Collection, Product
from nxtbn.product.models import Supplier
from nxtbn.core.currency.backend import currency_Backend


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    summary = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    category = filters.ModelChoiceFilter(field_name='category', queryset=Category.objects.all())
    supplier = filters.ModelChoiceFilter(field_name='supplier', queryset=Supplier.objects.all())
    brand = filters.CharFilter(lookup_expr='icontains')
    type = filters.CharFilter(field_name='type', lookup_expr='exact')
    related_to = filters.CharFilter(field_name='related_to__name', lookup_expr='icontains')
    collection = filters.ModelChoiceFilter(field_name='collections', queryset=Collection.objects.all())

    class Meta:
        model = Product
        fields = ('name', 'summary', 'description', 'category', 'supplier', 'brand', 'type', 'related_to', 'collection')


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = NxtbnPagination
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]
    filterset_class = ProductFilter
    ordering_fields = ['name', 'created_at']
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['exchange_rate'] = self.get_exchange_rate()
        return context

    def get_exchange_rate(self):
        if settings.IS_MULTI_CURRENCY:
            return currency_Backend().get_exchange_rate(self.request.currency)
        return 1.0


    def paginate_and_serialize(self, queryset): # NXTBN specific
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return  ProductWithDefaultVariantSerializer
        
        if self.action == 'retrieve':
            return ProductDetailSerializer
        
        if self.action == 'with_related':
            return ProductDetailWithRelatedLinkMinimalSerializer

        return ProductWithVariantSerializer
        

    @action(detail=False, methods=['get'], url_path='withvariant')
    def withvariant(self, request):
        queryset = self.filter_queryset(self.queryset)
        return self.paginate_and_serialize(queryset)
    
    @action(detail=True, methods=['get'], url_path='with-related')
    def with_related(self, request, slug=None):
        queryset = self.filter_queryset(self.queryset.filter(slug=slug))
        return self.paginate_and_serialize(queryset)

    

class CollectionListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = None
    queryset = Collection.objects.filter(is_active=True)
    serializer_class = CollectionSerializer

class CategoryListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = None
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'