from django.urls import path, include, register_converter
from rest_framework.routers import DefaultRouter

from nxtbn.core.url_converters import IdOrNoneConverter

from nxtbn.product.api.dashboard.views import (
    CategoryNameView,
    CategoryTranslationViewSet,
    CollectionNameView,
    CollectionTranslationViewSet,
    ProductListView,
    ProductDetailView,
    CategoryListView,
    CategoryByParentView,
    CategoryDetailView,
    CollectionViewSet,
    ProductNameView,
    ProductTagNameView,
    ProductTagTranslationViewSet,
    ProductTranslationDetails,
    RecursiveCategoryListView,
    ColorViewSet,
    ProductTypeViewSet,
    ProductTagViewSet,
    ProductVariantDeleteAPIView,
    ProductWithVariantView,
    ProductMinimalListView,
    ProductListDetailVariantView,
    SupplierNameView,
    SupplierTranslationViewSet,
    TaxClassView,
    BulkProductStatusUpdateAPIView,
    BulkProductDeleteAPIView,
    ProductVariants,
    InventoryListView,
    SupplierModelViewSet
)

register_converter(IdOrNoneConverter, 'id_or_none')


router = DefaultRouter()
router.register(r'colors', ColorViewSet)
router.register(r'product-types', ProductTypeViewSet)
router.register(r'product-tags', ProductTagViewSet)
router.register(r'collections', CollectionViewSet)
router.register(r'suppliers', SupplierModelViewSet)

# Translation views
router.register(r'supplier-translations', SupplierTranslationViewSet, basename='supplier-translation')
router.register(r'category-translations', CategoryTranslationViewSet, basename='category-translation')
router.register(r'collection-translations', CollectionTranslationViewSet, basename='collection-translation')
router.register(r'product-tag-translations', ProductTagTranslationViewSet, basename='product-tag-translation')

urlpatterns = [
    path('', include(router.urls)),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/minimal/', ProductMinimalListView.as_view(), name='product-minimal-list'),
    path('products/with-detailed-variants/', ProductListDetailVariantView.as_view(), name='product-list-with-detailed-variants'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('product-with-variants/<int:id>/', ProductWithVariantView.as_view(), name='product-with-variant'),
    path('variants/<int:pk>/', ProductVariantDeleteAPIView.as_view(), name='variant-delete'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('recursive-categories/', RecursiveCategoryListView.as_view(), name='recursive-category'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories-by-parent/<id_or_none:id>/', CategoryByParentView.as_view(), name='category-by-parent'),
    path('tax-class/', TaxClassView.as_view(), name='tax-class'),
    path('products/update/bulk/', BulkProductStatusUpdateAPIView.as_view(), name='bulk-product-status-update'),
    path('products/delete/bulk/', BulkProductDeleteAPIView.as_view(), name='bulk-product-status-delete'),
    path('products-variants/', ProductVariants.as_view(), name='products-variants'),
    path('inventory/', InventoryListView.as_view(), name='product-inventory'),

    # Translation
    path('product-translations/<int:base_product_id>/<str:lang_code>/', ProductTranslationDetails.as_view(), name='product-translation'),

    # Name and id views
    path('products-name/', ProductNameView.as_view(), name='product-list-name'),
    path('categories-name/', CategoryNameView.as_view(), name='category-list-name'),
    path('suppliers-name/', SupplierNameView.as_view(), name='supplier-list-name'),
    path('product-tags-name/', ProductTagNameView.as_view(), name='product-tag-list-name'),
    path('collections-name/', CollectionNameView.as_view(), name='collection-list-name'),
]

