from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from nxtbn.order import OrderStatus
from nxtbn.users import UserRole

from babel.numbers import get_currency_precision, format_currency


class User(AbstractUser):
    role = models.CharField(max_length=255, choices=UserRole.choices, default=UserRole.CUSTOMER)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        parts = [self.get_full_name(), self.username, self.email, self.get_role_display()]
        return " - ".join(part for part in parts if part)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def total_spent(self):
        precision = get_currency_precision(settings.BASE_CURRENCY)
        total_spent_in_subunit =  self.payments.aggregate(models.Sum('payment_amount'))['payment_amount__sum'] or 0
        total_spent_in_unit = total_spent_in_subunit / (10 ** precision)
        total_spent = format_currency(total_spent_in_unit, settings.BASE_CURRENCY, locale='en_US')
        return total_spent

    
    def total_order_count(self):
        return self.orders.count()
    
    def total_cancelled_order_count(self):
        return self.orders.filter(status=OrderStatus.CANCELLED).count()
    
    def total_pending_order_count(self):
        return self.orders.filter(status=OrderStatus.PENDING).count()
    
    def total_refunded_order_count(self):
        return self.orders.filter(status=OrderStatus.REFUNDED).count()
    