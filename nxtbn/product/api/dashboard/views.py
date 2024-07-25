from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions  import AllowAny
from rest_framework.exceptions import APIException
from rest_framework import viewsets


from nxtbn.core.paginator import NxtbnPagination
from nxtbn.product.models import Color, Product, Category, Collection, ProductTag, ProductType
from nxtbn.product.api.dashboard.serializers import (
    BasicCategorySerializer,
    ColorSerializer,
    ProductCreateSerializer,
    ProductDetailsSerializer,
    ProductSerializer,
    CategorySerializer,
    CollectionSerializer,
    ProductTagSerializer,
    ProductTypeSerializer,
    RecursiveCategorySerializer
)
from nxtbn.core.admin_permissions import NxtbnAdminPermission



class ProductListView(generics.ListCreateAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = NxtbnPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    permission_classes = (NxtbnAdminPermission,)
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


class CollectionListView(generics.ListCreateAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (NxtbnAdminPermission,)
    pagination_class = None


class CollectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (NxtbnAdminPermission,)
    lookup_field = 'id'


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

    def get_queryset(self):
        return ProductTag.objects.all()