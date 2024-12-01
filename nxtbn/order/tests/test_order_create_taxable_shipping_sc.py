import random
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from nxtbn.core import PublishableStatus
from nxtbn.core.utils import normalize_amount_currencywise
from nxtbn.home.base_tests import BaseTestCase
from nxtbn.product import WeightUnits
from nxtbn.product.models import Product, ProductType
from rest_framework.test import APIClient
from nxtbn.product.tests import ProductFactory, ProductTypeFactory, ProductVariantFactory
from nxtbn.shipping.tests import ShippingMethodFactory, ShippingRateFactory
from nxtbn.tax.tests import TaxClassFactory


class OrderCreateShippingRate(BaseTestCase):
    """
    Test case for Order Create API with a single currency mode.
    Ensures accurate shipping rates calculation for products based on weight and regions.
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.login(email='test@example.com', password='testpass')

        # Define regions and countries
        self.country = "US"
        self.state_one = "TX"
        self.state_two = "NY"

        # Tax class
        self.tax_class = TaxClassFactory()

        # API endpoints
        self.order_api_url = reverse('order-create')
        self.order_estimate_api_url = reverse('order-estimate')

    def _test_order_for_currency(self, currency, params_list):
        """
        Helper method to test order creation and estimation for a given currency.
        """
        for params in params_list:
            # Product setup
            product_type = ProductTypeFactory(
                name=f"{currency} Product Type",
                track_stock=False,
                taxable=True,
                physical_product=True,
                weight_unit=WeightUnits.KILOGRAM,
            )
            product = ProductFactory(
                product_type=product_type,
                tax_class=self.tax_class,
                status=PublishableStatus.PUBLISHED,
            )

            # Variant setup
            variant = ProductVariantFactory(
                product=product,
                track_inventory=False,
                currency=currency,
                price=normalize_amount_currencywise(params['price'], currency),
                cost_per_unit=params['cost_per_unit'],
            )

            # Shipping method and rates
            shipping_method = ShippingMethodFactory(name="DHL-EXPRESS")
            shipping_rate = ShippingRateFactory(
                shipping_method=shipping_method,
                country=self.country,
                region=params['region'],
                rate=normalize_amount_currencywise(params['shipping_rate'], currency),
                weight_min=0,
                weight_max=5,
                currency=currency,
            )

            # Order payload
            order_payload = {
                "shipping_address": {
                    "country": self.country,
                    "state": params['region'],
                    "street_address": "123 Main St",
                    "city": "Test City",
                    "postal_code": "12345",
                    "email": "customer@example.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "phone_number": "1234567890",
                },
                "variants": [
                    {"alias": variant.alias, "quantity": params["quantity"]},
                ],
            }

            # Estimate API call
            estimate_response = self.client.post(self.order_estimate_api_url, order_payload, format='json')
            self.assertEqual(estimate_response.status_code, status.HTTP_200_OK)
            self.assertEqual(estimate_response.data['subtotal'], params['expected_subtotal'])
            self.assertEqual(estimate_response.data['total'], params['expected_total'])

            # Order Create API call
            order_response = self.client.post(self.order_api_url, order_payload, format='json')
            self.assertEqual(order_response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(order_response.data['subtotal'], params['expected_subtotal'])
            self.assertEqual(order_response.data['total'], params['expected_total'])

    def test_order_for_all_currencies(self):
        """
        Test order creation and estimation for multiple currencies.
        """
        currencies = {
            "USD": [
                {
                    "price": 20.0,
                    "cost_per_unit": 15.0,
                    "shipping_rate": 10.0,
                    "region": self.state_two,
                    "quantity": 3,
                    "expected_subtotal": "$60.00",
                    "expected_total": "$70.00",
                },
            ],
            "JPY": [
                {
                    "price": 2000,
                    "cost_per_unit": 1500,
                    "shipping_rate": 1000,
                    "region": self.state_two,
                    "quantity": 3,
                    "expected_subtotal": "¥6,000",
                    "expected_total": "¥7,000",
                },
            ],
            "KWD": [
                {
                    "price": 6.0,
                    "cost_per_unit": 5.0,
                    "shipping_rate": 1.0,
                    "region": self.state_one,
                    "quantity": 10,
                    "expected_subtotal": "KD 60.000",
                    "expected_total": "KD 70.000",
                },
            ],
        }

        for currency, params_list in currencies.items():
            self._test_order_for_currency(currency, params_list)
