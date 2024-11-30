import random
import sys
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from nxtbn.core import PublishableStatus
from nxtbn.core.utils import normalize_amount_currencywise
from nxtbn.home.base_tests import BaseTestCase
from django.utils import timezone
from nxtbn.product.models import Product, ProductType
from rest_framework.test import APIClient
from nxtbn.product.tests import ProductFactory, ProductTypeFactory, ProductVariantFactory
from nxtbn.tax.tests import TaxClassFactory, TaxRateFactory


class OrderCreateMultiCurrencyAPI(BaseTestCase):
    """
    Test Case for Order Create API with multiple currencies: USD, JPY, KD.
    This test ensures accuracy of calculations and multi-precision handling for different currencies.
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.login(email='test@example.com', password='testpass')

        # Define common properties
        self.country = 'US'
        self.state = 'NY'

        # Tax class and rate
        self.tax_class = TaxClassFactory()
        self.tax_rate = TaxRateFactory(
            tax_class=self.tax_class,
            is_active=True,
            rate=15,  # 15%
            country=self.country,
            state=self.state,
        )

        # Product type
        self.product_type = ProductTypeFactory(
            name="Multi-currency product",
            track_stock=False,
            taxable=True,
        )

        # Product
        self.product = ProductFactory(
            product_type=self.product_type,
            tax_class=self.tax_class,
            status=PublishableStatus.PUBLISHED,
        )

        # Variants based on the base currency in settings
        self.variants = {}

        # USD Variant
        if settings.BASE_CURRENCY == "USD":
            self.variants["USD"] = ProductVariantFactory(
                product=self.product,
                track_inventory=False,
                currency="USD",
                price=normalize_amount_currencywise(20.26, "USD"),
                stock=10,
                cost_per_unit=50,
            )

        # JPY Variant
        elif settings.BASE_CURRENCY == "JPY":
            self.variants["JPY"] = ProductVariantFactory(
                product=self.product,
                track_inventory=False,
                currency="JPY",
                price=normalize_amount_currencywise(2000, "JPY"),  # ¥2000 JPY
                stock=10,
                cost_per_unit=5000,
            )

        # KWD Variant
        elif settings.BASE_CURRENCY == "KWD":
            self.variants["KWD"] = ProductVariantFactory(
                product=self.product,
                track_inventory=False,
                currency="KWD",
                price=normalize_amount_currencywise(20.234, "KWD"),  # KD 20.234
                stock=10,
                cost_per_unit=50.500,
            )

        self.order_api_url = reverse('order-create')
        self.order_estimate_api_url = reverse('order-eastimate')

    def _test_order_for_currency(self, currency, expected_values):
        """
        Helper method to test order create and estimate for a specific currency.
        """
        variant = self.variants[currency]
        order_payload = {
            "shipping_address": {
                "country": self.country,
                "state": self.state,
                "street_address": "123 Main St",
                "city": "New York",
                "postal_code": "10001",
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "1234567890"
            },
            "billing_address": {
                "country": self.country,
                "state": self.state,
                "street_address": "123 Main St",
                "city": "New York",
                "postal_code": "10001",
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "1234567890"
            },
            "variants": [
                {
                    "alias": variant.alias,
                    "quantity": 3,
                }
            ]
        }

        # Estimate Test
        order_estimate_response = self.client.post(self.order_estimate_api_url, order_payload, format='json')
        self.assertEqual(order_estimate_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_estimate_response.data['subtotal'], expected_values['subtotal'])
        self.assertEqual(order_estimate_response.data['total'], expected_values['total'])
        self.assertEqual(order_estimate_response.data['estimated_tax'], expected_values['tax'])
        # self.assertEqual(order_estimate_response.data['discount'], '$0.00')
        # self.assertEqual(order_estimate_response.data['total_items'], 3)
        # self.assertEqual(order_estimate_response.data['shipping_fee'], '$0.00')

        # Order Create Test
        order_response = self.client.post(self.order_api_url, order_payload, format='json')
        self.assertEqual(order_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_response.data['subtotal'], expected_values['subtotal'])
        self.assertEqual(order_response.data['total'], expected_values['total'])
        self.assertEqual(order_response.data['estimated_tax'], expected_values['tax'])
        # self.assertEqual(order_response.data['discount'], '$0.00')
        # self.assertEqual(order_response.data['total_items'], 3)
        # self.assertEqual(order_response.data['shipping_fee'], '$0.00')

    def test_order_for_all_currencies(self):
        """
        Test order creation and estimation for all currencies: USD, JPY, KD.
        """
        # USD
        if settings.BASE_CURRENCY == "USD":
            self._test_order_for_currency(
                "USD",
                {
                    "subtotal": "$60.78",
                    "total": "$69.90",
                    "tax": "$9.12",
                },
            )

        # JPY
        elif settings.BASE_CURRENCY == "JPY":
            self._test_order_for_currency(
                "JPY",
                {
                    "subtotal": "¥6,000",
                    "total": "¥6,900",
                    "tax": "¥900",
                },
            )

        # KD
        elif settings.BASE_CURRENCY == "KWD":
            self._test_order_for_currency(
                "KWD",
                {
                    "subtotal": "KWD60.702",
                    "total": "KWD69.807",
                    "tax": "KWD 9.105",
                },
            )
