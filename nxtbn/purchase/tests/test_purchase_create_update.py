import random
from decimal import Decimal
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from nxtbn.core import PublishableStatus
from nxtbn.core.utils import build_currency_amount, normalize_amount_currencywise
from nxtbn.home.base_tests import BaseTestCase
from nxtbn.order.proccesor.views import get_shipping_rate_instance
from nxtbn.product import WeightUnits
from nxtbn.product.models import Product
from rest_framework.test import APIClient
from nxtbn.product.tests import ProductFactory, ProductTypeFactory, ProductVariantFactory, SupplierFactory
from nxtbn.purchase import PurchaseStatus
from nxtbn.purchase.models import PurchaseOrderItem
from nxtbn.purchase.tests import PurchaseOrderFactory, PurchaseOrderItemFactory
from nxtbn.shipping.models import ShippingRate
from nxtbn.shipping.tests import ShippingMethodFactory, ShippingRateFactory
from nxtbn.tax.tests import TaxClassFactory, TaxRateFactory
from babel.numbers import get_currency_precision, format_currency


from django.test.utils import override_settings

from nxtbn.warehouse.models import Stock
from nxtbn.warehouse.tests import StockFactory, WarehouseFactory
from datetime import date


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class PurchageCreateUpdateAPITest(BaseTestCase):
   
    def setUp(self):
        super().setUp()
        self.adminLogin()

        self.supplier = SupplierFactory()
        self.warehouse = WarehouseFactory()
        self.product = ProductFactory()
        self.product_variant_one = ProductVariantFactory(
            product=self.product,
            price=Decimal('100.00'),
            cost_per_unit=Decimal('100.00')
        )
        self.product_variant_two = ProductVariantFactory(
            product=self.product,
            price=Decimal('100.00'),
            cost_per_unit=Decimal('100.00')
        )
        self.product_variant_three = ProductVariantFactory(
            product=self.product,
            price=Decimal('100.00'),
            cost_per_unit=Decimal('100.00')
        )
        self.product_variant_four = ProductVariantFactory(
            product=self.product,
            price=Decimal('100.00'),
            cost_per_unit=Decimal('100.00')
        )

       

    def test_purchange_create_update(self):

        purchage_create_url = reverse('purchaseorder-list')