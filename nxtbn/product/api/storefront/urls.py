from django.urls import path
from rest_framework.routers import DefaultRouter

from nxtbn.product.api.storefront import views as product_views
from django.urls import include

router = DefaultRouter()
router.register(r'products', product_views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('products/<slug:slug>/with-recommended/', product_views.RecommendedProductWiseListView.as_view(), name='product-recommended-list-product-wise'),
    path('collections/', product_views.CollectionListView.as_view(), name='collection-list'),
    path('recursive-categories/', product_views.CategoryListView.as_view(), name='category-list'),
]
