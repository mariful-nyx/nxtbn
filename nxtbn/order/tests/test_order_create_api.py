import random
import sys
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from nxtbn.core import PublishableStatus
from nxtbn.core.utils import normalize_amount_currencywise
from nxtbn.home.base_tests import BaseTestCase
from nxtbn.product.models import Product, ProductType
from rest_framework.test import APIClient
from nxtbn.product.tests import ProductFactory, ProductTypeFactory, ProductVariantFactory
from nxtbn.tax.tests import TaxClassFactory, TaxRateFactory


class OrderCreateMultiCurrencyAPI(BaseTestCase):
    """
    Test Case for Order Create API with multiple currencies: USD, JPY, KWD.
    This test ensures accuracy of calculations and multi-precision handling for different currencies.
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.login(email='test@example.com', password='testpass')

        # Define common properties
        self.country = 'US'
        self.state = 'NY'

        # Tax class
        self.tax_class = TaxClassFactory()

        self.order_api_url = reverse('order-create')
        self.order_estimate_api_url = reverse('order-eastimate')

    def _test_order_for_currency(self, currency, params):
        """
        Helper method to test order create and estimate for a specific currency.
        Dynamically creates a variant based on provided params.
        """
        # Set up tax rate
        tax_rate = TaxRateFactory(
            tax_class=self.tax_class,
            is_active=True,
            rate=params['tax_rate'],
            country=self.country,
            state=self.state,
        )

        # Create product type and product
        product_type = ProductTypeFactory(
            name=f"{currency} Product Type non trackable and taxable",
            track_stock=False,
            taxable=True,
        )
        product = ProductFactory(
            product_type=product_type,
            tax_class=self.tax_class,
            status=PublishableStatus.PUBLISHED,
        )

        # Create variant
        variant = ProductVariantFactory(
            product=product,
            track_inventory=False,
            currency=currency,
            price=normalize_amount_currencywise(params['price'], currency),
            stock=params['stock'],
            cost_per_unit=params['cost_per_unit'],
        )

        # Payload for order
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
        self.assertEqual(order_estimate_response.data['subtotal'], params['subtotal'])
        self.assertEqual(order_estimate_response.data['total'], params['total'])
        self.assertEqual(order_estimate_response.data['estimated_tax'], params['tax'])

        # Order Create Test
        order_response = self.client.post(self.order_api_url, order_payload, format='json')
        self.assertEqual(order_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_response.data['subtotal'], params['subtotal'])
        self.assertEqual(order_response.data['total'], params['total'])
        self.assertEqual(order_response.data['estimated_tax'], params['tax'])

    def test_order_for_all_currencies(self):
        """
        Test order creation and estimation for all currencies: USD, JPY, KWD.
        """
        # USD Test
        if settings.BASE_CURRENCY == 'USD':
            self._test_order_for_currency(
                "USD",
                {
                    # Expected output
                    "subtotal": "$60.78",
                    "total": "$69.90",
                    "tax": "$9.12",

                    # Variant creation parameters
                    "price": 20.26,
                    "cost_per_unit": 50.00,
                    "tax_rate": 15,  # 15%
                    "stock": 10,
                },
            )

        # JPY Test
        if settings.BASE_CURRENCY == 'JPY':
            self._test_order_for_currency(
                "JPY",
                {
                    # Expected output
                    "subtotal": "¥6,000",
                    "total": "¥6,900",
                    "tax": "¥900",

                    # Variant creation parameters
                    "price": 2000,
                    "cost_per_unit": 5000,
                    "tax_rate": 15,  # 15%
                    "stock": 10,
                },
            )

        if settings.BASE_CURRENCY == 'KWD':
            self._test_order_for_currency(
                "KWD",
                {
                    # Expected output
                    "subtotal": "KWD60.702",
                    "total": "KWD69.807",
                    "tax": "KWD9.105",

                    # Variant creation parameters
                    "price": 20.234,
                    "cost_per_unit": 15.500,
                    "tax_rate": 15,  # 15%
                    "stock": 10,
                },
            )

        # if not USD, JPY, KWD, skip the test as these 3 currencies are enough to test multi-currency handling as they have different precision