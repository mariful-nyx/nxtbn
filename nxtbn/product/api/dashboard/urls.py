from django.urls import path, include
from rest_framework.routers import DefaultRouter

from nxtbn.product.api.dashboard.views import (
    ProductListView,
    ProductDetailView,
    CategoryListView,
    CategoryByParentView,
    CategoryDetailView,
    CollectionListView,
    CollectionDetailView,
    RecursiveCategoryListView,
    ColorViewSet
)

router = DefaultRouter()
router.register(r'colors', ColorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('recursive-categories/', RecursiveCategoryListView.as_view(), name='recursive-category'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories-by-parent/<int:id>/', CategoryByParentView.as_view(), name='category-by-parent'),

    path('collections/', CollectionListView.as_view(), name='collection-list'),
    path('collections/<int:id>/', CollectionDetailView.as_view(), name='collection-detail'),
]

