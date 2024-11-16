from django.forms import ValidationError
from django.db.models import Sum, F

from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions  import AllowAny
from rest_framework.exceptions import APIException
from rest_framework import viewsets

from rest_framework import filters as drf_filters
import django_filters
from django_filters import rest_framework as filters

from nxtbn.core import PublishableStatus
from nxtbn.core.paginator import NxtbnPagination
from nxtbn.product.models import Color, Product, Category, Collection, ProductTag, ProductType, ProductVariant
from nxtbn.product.api.dashboard.serializers import (
    BasicCategorySerializer,
    ColorSerializer,
    ProductCreateSerializer,
    ProductMinimalSerializer,
    ProductMutationSerializer,
    ProductSerializer,
    CategorySerializer,
    CollectionSerializer,
    ProductStatusDeleteBulkSerializer,
    ProductStatusUpdateBulkSerializer,
    ProductTagSerializer,
    ProductTypeSerializer,
    ProductWithVariantSerializer,
    RecursiveCategorySerializer,
    TaxClassSerializer
)
from nxtbn.core.admin_permissions import NxtbnAdminPermission, RoleBasedPermission
from nxtbn.tax.models import TaxClass
from nxtbn.users import UserRole


class ProductFilter(filters.FilterSet):
    currency = filters.CharFilter(field_name='currency', lookup_expr='iexact')
    variant_alias = filters.CharFilter(field_name='variants__alias', lookup_expr='iexact')
    variant_sku = filters.CharFilter(field_name='variants__sku', lookup_expr='iexact')
    created_at = filters.DateFromToRangeFilter(field_name='created_at') # eg. ?created_at_after=2023-09-01&created_at_before=2023-09-12
    promo_code = filters.CharFilter(field_name='promo_codes__code', lookup_expr='iexact')

    class Meta:
        model = Product
        fields = [
            'id',
            'alias',
            'variant_alias',
            'variant_sku',
            'name',
            'currency',
            'category',
            'supplier',
            'brand',
            'product_type',
            'collections',
            'tags',
            'created_at',
            'promo_code',
            'status',
        ]



class ProductFilterMixin:
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter
    ] 
    search_fields = [
        'name',
        'brand',
        'supplier__name',
        'category__name',
        'product_type__name',
        'collections__name',
    ]
    ordering_fields = [
        'name',
        'created_at',
        'status',
        'default_variant__price',
        'total_sales'
    ]
    filterset_class = ProductFilter

    def get_queryset(self):
        if self.request.query_params.get('ordering', '') in ['total_sales', '-total_sales']:
            return Product.objects.all().annotate(
                total_sales=Sum(F('variants__orderlineitems__quantity'))
            )
        return Product.objects.all()

class ProductListView(ProductFilterMixin, generics.ListCreateAPIView):
    permission_classes = (NxtbnAdminPermission,)
    serializer_class = ProductSerializer
    pagination_class = NxtbnPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductSerializer

class ProductMinimalListView(ProductFilterMixin, generics.ListAPIView):
    permission_classes = (NxtbnAdminPermission,)
    serializer_class = ProductMinimalSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        # Get the filtered queryset first
        queryset = self.filter_queryset(self.get_queryset()).filter(status=PublishableStatus.PUBLISHED)

        # Limit the results to a maximum of 10
        limited_queryset = queryset[:10]
        serializer = self.get_serializer(limited_queryset, many=True)
        return Response(serializer.data)

    
class ProductListDetailVariantView(ProductFilterMixin, generics.ListAPIView):
    serializer_class = ProductWithVariantSerializer
    pagination_class = NxtbnPagination

    permission_classes = (RoleBasedPermission,)
    ROLE_PERMISSIONS = {
        UserRole.STORE_MANAGER: {"list",},
        UserRole.ORDER_PROCESSOR: {"list",},
        UserRole.CUSTOMER_SUPPORT_AGENT: {"list",},
        UserRole.MARKETING_MANAGER: {"list",},
    }
    action = 'list'
        
    def get_queryset(self):
        return Product.objects.filter(status=PublishableStatus.PUBLISHED)

    

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Product.objects.all()
    serializer_class = ProductMutationSerializer
    lookup_field = 'id'

class ProductWithVariantView(generics.RetrieveAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Product.objects.all()
    serializer_class = ProductWithVariantSerializer
    lookup_field = 'id'


class CategoryListView(generics.ListCreateAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Category.objects.filter()
    serializer_class = CategorySerializer


class RecursiveCategoryListView(generics.ListCreateAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Category.objects.filter(parent=None) # Get only top-level categories
    serializer_class = RecursiveCategorySerializer
    pagination_class = None

class CategoryByParentView(generics.ListAPIView):
    pagination_class = None
    permission_classes = (NxtbnAdminPermission,)
    queryset = Category.objects.all()
    serializer_class = BasicCategorySerializer
    permission_classes = (NxtbnAdminPermission,)
    
    def get_queryset(self):
        return super().get_queryset().filter(parent=self.kwargs.get('id'))

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (NxtbnAdminPermission,)
    lookup_field = 'id'

class CollectionViewSet(viewsets.ModelViewSet):
    pagination_class = None
    permission_classes = (NxtbnAdminPermission,)
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Collection.objects.all()
    
class ColorViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    allowed_methods = ['GET', 'POST', 'DELETE']

    def get_queryset(self):
        return Color.objects.all()
    

class ProductTypeViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

    def get_queryset(self):
        return ProductType.objects.all()
    

class ProductTagViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    filter_backends = [
        drf_filters.SearchFilter,
    ]
    search_fields = ['name']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = response.data[:5]
        return response
    

class ProductVariantDeleteAPIView(generics.DestroyAPIView):
    queryset = ProductVariant.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the variant is the default variant of any product
        if instance.product.default_variant == instance:
            raise ValidationError("This variant is set as the default variant for a product and cannot be deleted.")
        
        # If not the default variant, proceed with deletion
        return super().destroy(request, *args, **kwargs)


class TaxClassView(generics.ListCreateAPIView):
    queryset = TaxClass.objects.all()
    serializer_class = TaxClassSerializer
    permission_classes = (NxtbnAdminPermission,)
    pagination_class = None


class BulkProductStatusUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProductStatusUpdateBulkSerializer
    permission_classes = (NxtbnAdminPermission,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_status = serializer.validated_data['status']
        product_ids = serializer.validated_data['product_ids']

        Product.objects.filter(id__in=product_ids).update(status=product_status)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BulkProductDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Product.objects.all()
    serializer_class = ProductStatusDeleteBulkSerializer

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_ids = serializer.validated_data['product_ids']
        Product.objects.filter(id__in=product_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)