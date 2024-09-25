from django.urls import path
from nxtbn.shipping.api.dashboard.views import CustomerEligibleShippingMethodstAPI

urlpatterns = [
    path('customer/eligible-shipping-rate/', CustomerEligibleShippingMethodstAPI.as_view(), name='customer-shipping-methods'),
]
