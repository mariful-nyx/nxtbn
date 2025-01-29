from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions  import AllowAny
from rest_framework.exceptions import APIException

from nxtbn.core.admin_permissions import NxtbnAdminPermission, RoleBasedHTTPMethodPermission
from nxtbn.payment.models import Payment
from nxtbn.payment.api.dashboard.serializers import PaymentCreateSerializer, RefundSerializer
from nxtbn.users import UserRole

class RefundAPIView(generics.UpdateAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Payment.objects.all()
    serializer_class = RefundSerializer

    permission_classes = (RoleBasedHTTPMethodPermission,)
    HTTP_PERMISSIONS = {
        UserRole.STORE_MANAGER: {"all"},
        UserRole.ADMIN: {"all"},
        UserRole.ORDER_PROCESSOR: {"get"},
        UserRole.ACCOUNTANT: {"all"},
    }

    def get_object(self):
        order_alias = self.kwargs.get('order_alias')
        return get_object_or_404(Payment, order__alias=order_alias)
    
class PaymentCreateAPIView(generics.CreateAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer

    permission_classes = (RoleBasedHTTPMethodPermission,)
    HTTP_PERMISSIONS = {
        UserRole.STORE_MANAGER: {"all"},
        UserRole.ADMIN: {"all"},
        UserRole.ORDER_PROCESSOR: {"get"},
        UserRole.ACCOUNTANT: {"all"},
    }