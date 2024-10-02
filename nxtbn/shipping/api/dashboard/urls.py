from django.urls import path
from nxtbn.shipping.api.dashboard.views import (
    CustomerEligibleShippingMethodstAPI, 
    CustomerEligibleShippingMethodDetail,
    ShippingRateView,
    ShippingRateDetailView
)

urlpatterns = [
    path('customer/eligible-shipping-method/', CustomerEligibleShippingMethodstAPI.as_view(), name='customer-shipping-methods'),
    path('customer/eligible-shipping-method/<int:id>/', CustomerEligibleShippingMethodDetail.as_view(), name='customer-shipping-method-detail'),
    path('customer/eligible-shipping-method/<int:shipping_method_id>/shipping-rates/', ShippingRateView.as_view(), name='shipping-rate-view'),
    path('customer/shipping-rates/<int:id>/', ShippingRateDetailView.as_view(), name='shipping-rate-detail-view'),

]
