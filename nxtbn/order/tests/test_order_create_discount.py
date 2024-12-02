import random
from decimal import Decimal
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from nxtbn.core import PublishableStatus
from nxtbn.core.utils import build_currency_amount, normalize_amount_currencywise
from nxtbn.discount import PromoCodeType
from nxtbn.discount.tests import PromoCodeFactory
from nxtbn.home.base_tests import BaseTestCase
from nxtbn.order.proccesor.views import get_shipping_rate_instance
from nxtbn.product import WeightUnits
from nxtbn.product.models import Product
from rest_framework.test import APIClient
from nxtbn.product.tests import ProductFactory, ProductTypeFactory, ProductVariantFactory
from nxtbn.shipping.models import ShippingRate
from nxtbn.shipping.tests import ShippingMethodFactory, ShippingRateFactory
from nxtbn.tax.tests import TaxClassFactory, TaxRateFactory
from babel.numbers import get_currency_precision, format_currency


class TestOrderCreateWithDiscountRate(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.login(email='test@example.com', password='testpass')

        self.country = 'US'
        self.state = 'NY'
        self.precision = str(get_currency_precision(settings.BASE_CURRENCY))
        

        self.test_cases = {
            '2': { # USD, EUR, BDT etc.
                'input_weight_min': 0,
                'input_weight_max': 5,  # 5kg
                'order_discount_code': 'DISCOUNT10P',

                'variant_one_price': 50.29,
                'variant_one_wv': 100,  # 100 grams
                'variant_one_oqty': 40,
                'variant_two_price': 20.26,
                'variant_two_wv': 578,
                'variant_two_oqty': 1,
                
            },
            '3': { # KWD, OMR, etc.
                'input_weight_min': 0,
                'input_weight_max': 5,  # 5kg
                'order_discount_code': 'DISCOUNT10P',

                'variant_one_price': 50.290,
                'variant_one_wv': 100,  # 100 grams
                'variant_one_oqty': 40,
                'variant_two_price': 20.260,
                'variant_two_wv': 578,
                'variant_two_oqty': 1,
            },
            '0': { # JPY, KRW, etc.
                'input_weight_min': 0,
                'input_weight_max': 5,  # 5kg
                'order_discount_code': 'DISCOUNT10P',

                'variant_one_price': 50,
                'variant_one_wv': 100,  # 100 grams
                'variant_one_oqty': 40,
                'variant_two_price': 20,
                'variant_two_wv': 578,
                'variant_two_oqty': 1,
            },
        }


        self.order_api_url = reverse('order-create')
        self.order_estimate_api_url = reverse('order-estimate')

        self.discount = PromoCodeFactory(
            code=self.test_cases[self.precision]['order_discount_code'],
            code_type=PromoCodeType.PERCENTAGE,
            value=10,
            is_active=True,
            min_purchase_amount=0,
            min_purchase_period=None,
            redemption_limit=None,
        )

    def test_order_discount_calculation(self):
        """
        Test case to ensure shipping rates are accurately calculated based on product weights and regions.
        """
        currency = settings.BASE_CURRENCY

        # Create product type and products
        product_type = ProductTypeFactory(
            name=f"{currency} Product Type physical",
            track_stock=False,
            taxable=False,
            physical_product=True,
        )


        # Create products and variants
        product_one = ProductFactory(
            product_type=product_type,
            status=PublishableStatus.PUBLISHED,
        )
        variant_one = ProductVariantFactory(
            product=product_one,
            track_inventory=False,
            currency=currency,
            price=normalize_amount_currencywise(self.test_cases[self.precision]['variant_one_price'], currency),
            cost_per_unit=50.00,
            weight_value= self.test_cases[self.precision]['variant_one_wv'],
        )
        
        product_two = ProductFactory(
            product_type=product_type,
            status=PublishableStatus.PUBLISHED,
        )
        variant_two = ProductVariantFactory(
            product=product_two,
            track_inventory=False,
            currency=currency,
            price=normalize_amount_currencywise(self.test_cases[self.precision]['variant_two_price'], currency),
            cost_per_unit=50.00,
            weight_value=self.test_cases[self.precision]['variant_two_wv'],  # 578 grams
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
            "promocode": self.test_cases[self.precision]['order_discount_code'],
            "variants": [
                {
                    "alias": variant_one.alias,
                    "quantity": self.test_cases[self.precision]['variant_one_oqty'],
                },
                {
                    "alias": variant_two.alias,
                    "quantity": self.test_cases[self.precision]['variant_two_oqty'],
                }
            ]
        }

        subtotal = Decimal(
            self.test_cases[self.precision]['variant_one_price'] * self.test_cases[self.precision]['variant_one_oqty'] +
            self.test_cases[self.precision]['variant_two_price'] * self.test_cases[self.precision]['variant_two_oqty']
        )
        total_discount = subtotal * Decimal(self.discount.value) / 100

       
        expected_subtotal = Decimal(
            self.test_cases[self.precision]['variant_one_price'] * self.test_cases[self.precision]['variant_one_oqty'] +
            self.test_cases[self.precision]['variant_two_price'] * self.test_cases[self.precision]['variant_two_oqty']
        )
        expected_total = expected_subtotal - total_discount


        expected_total_fr = build_currency_amount(expected_total, currency, locale='en_US')
        expected_subtotal_fr = build_currency_amount(expected_subtotal, currency, locale='en_US')
        expected_total_discount_fr = build_currency_amount(total_discount, currency, locale='en_US')
        

        

        # Estimate Test
        order_estimate_response = self.client.post(self.order_estimate_api_url, order_payload, format='json')

        self.assertEqual(order_estimate_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_estimate_response.data['subtotal'], expected_subtotal_fr)
        self.assertEqual(order_estimate_response.data['total'], expected_total_fr)
        self.assertEqual(order_estimate_response.data['discount'], expected_total_discount_fr)
       

        # Order Create Test
        order_response = self.client.post(self.order_api_url, order_payload, format='json')
        self.assertEqual(order_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_response.data['subtotal'], expected_subtotal_fr)
        self.assertEqual(order_response.data['total'], expected_total_fr)
        self.assertEqual(order_response.data['discount'], expected_total_discount_fr)
       
