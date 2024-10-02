from django.urls import path
from nxtbn.shipping.api.dashboard.views import (
    CustomerEligibleShippingMethodstAPI, 
    ShippingMethodDetails,
    ShippingRateListCreateView,
    ShippingRateDetailView, 
    ShippingMethodstListAPI
)

urlpatterns = [
    path('customer/eligible-shipping-method/', CustomerEligibleShippingMethodstAPI.as_view(), name='customer-shipping-methods'),
    path('shipping-methods/', ShippingMethodstListAPI.as_view(), name='customer-shipping-method-list'),
    path('shipping-method/<int:id>/', ShippingMethodDetails.as_view(), name='customer-shipping-method-detail'),

    path('shipping-rates/', ShippingRateListCreateView.as_view(), name='shipping-rate-view'),
    path('shipping-rates/<int:id>/', ShippingRateDetailView.as_view(), name='shipping-rate-detail-view'),

]
