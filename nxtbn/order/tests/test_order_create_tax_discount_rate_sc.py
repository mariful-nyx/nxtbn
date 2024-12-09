from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from nxtbn.core import PublishableStatus
from nxtbn.product.tests import ProductFactory, ProductTypeFactory, ProductVariantFactory
from nxtbn.tax.tests import TaxClassFactory, TaxRateFactory
from nxtbn.discount.tests import PromoCodeFactory, PromoCodeCustomer, PromoCodeProduct # Assuming promo codes are defined here
from nxtbn.home.base_tests import BaseTestCase
from nxtbn.core.utils import normalize_amount_currencywise

class OrderCreateMultiplePromoCodesTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.auth_client = APIClient()
        self.adminLogin()

        # Common setup
        self.country = 'US'
        self.state = 'NY'

        # Tax classes
        self.tax_class_15 = TaxClassFactory()
        self.tax_class_5 = TaxClassFactory()

        # Promo Codes
        self.promo_20all = PromoCodeFactory(code="20ALL", code_type="PERCENTAGE", value=20)  # 20% discount
        self.promo_flat200 = PromoCodeFactory(code="FLAT200ALL", code_type="FIXED", value=6)  # $6 flat discount
        self.promo_gold5 = PromoCodeFactory(code="GOLDCUSTOMER5", code_type="PERCENTAGE", value=5)  # 5% for Gold customers
        self.promo_sell5 = PromoCodeFactory(code="SELL5", code_type="PERCENTAGE", value=5, min_purchase_amount=500)
        self.promo_clearance20 = PromoCodeFactory(code="CLEARANCE20", code_type="PERCENTAGE", value=20, new_customers_only=True)

        self.order_api_url = reverse('admin_order_create')
        self.order_estimate_api_url = reverse('admin_order_estimate')

    def _create_order_with_promo(self, promo_code, currency, params):
        """
        Helper method to create orders with a specific promo code.
        """
        # Set up tax rates
        TaxRateFactory(tax_class=self.tax_class_15, is_active=True, rate=15, country=self.country, state=self.state)
        TaxRateFactory(tax_class=self.tax_class_5, is_active=True, rate=5, country=self.country, state=self.state)

        # Create products and variants with 6 properties
        products = []
        for i in range(1, 7):
            product = ProductFactory(
                product_type=ProductTypeFactory(
                    name=f"{currency} Product Type non trackable, taxable {5 * i}%",
                    track_stock=False,
                    taxable=True,
                ),
                tax_class=self.tax_class_5 if i % 2 == 0 else self.tax_class_15,
                status=PublishableStatus.PUBLISHED,
            )
            products.append(product)


        
        variant_1 = ProductVariantFactory(
            product=products[0], 
            track_inventory=False,
            currency=currency,
            price=normalize_amount_currencywise(params['variant_1']['price'], currency),
            stock=params['variant_1']['stock'],
            cost_per_unit=params['variant_1']['cost_per_unit']
        )
        variant_2 = ProductVariantFactory(
            product=products[1], 
            track_inventory=False,
            currency=currency,
            price=normalize_amount_currencywise(params['variant_1']['price'], currency),
            stock=params['variant_1']['stock'],
            cost_per_unit=params['variant_1']['cost_per_unit']
        )
        variant_3 = ProductVariantFactory(
            product=products[2], 
            track_inventory=False,
            currency=currency,
            price=normalize_amount_currencywise(params['variant_1']['price'], currency),
            stock=params['variant_1']['stock'],
            cost_per_unit=params['variant_1']['cost_per_unit']
        )
        variant_4 = ProductVariantFactory(
            product=products[3], 
            track_inventory=False,
            currency=currency,
            price=normalize_amount_currencywise(params['variant_1']['price'], currency),
            stock=params['variant_1']['stock'],
            cost_per_unit=params['variant_1']['cost_per_unit']
        )
        variant_5 = ProductVariantFactory(
            product=products[4], 
            track_inventory=False,
            currency=currency,
            price=normalize_amount_currencywise(params['variant_1']['price'], currency),
            stock=params['variant_1']['stock'],
            cost_per_unit=params['variant_1']['cost_per_unit']
        )
        variant_6 = ProductVariantFactory(
            product=products[5], 
            track_inventory=False,
            currency=currency,
            price=normalize_amount_currencywise(params['variant_1']['price'], currency),
            stock=params['variant_1']['stock'],
            cost_per_unit=params['variant_1']['cost_per_unit']
        )

        promocode_payload = {}

        if type(promo_code) == dict:
            promocode_payload = {
                'custom_discount_amount': promo_code
            }
        else:
            promocode_payload = {
                'promocode': promo_code
            }

            
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
            **promocode_payload,  # Applying promo code
            "variants": [
                {"alias": variant_1.alias, "quantity": 2},
                {"alias": variant_2.alias, "quantity": 3},
                {"alias": variant_3.alias, "quantity": 4},
                {"alias": variant_4.alias, "quantity": 6},
                {"alias": variant_5.alias, "quantity": 7},
                {"alias": variant_6.alias, "quantity": 8},
            ]
        }


        # Estimate Test
        order_estimate_response = self.auth_client.post(self.order_estimate_api_url, order_payload, format='json')

        self.assertEqual(order_estimate_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_estimate_response.data['subtotal'], params['subtotal'])
        self.assertEqual(order_estimate_response.data['total'], params['total'])
        self.assertEqual(order_estimate_response.data['estimated_tax'], params['tax'])

        # Order Create Test
        order_response = self.auth_client.post(self.order_api_url, order_payload, format='json')
        self.assertEqual(order_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_response.data['subtotal'], params['subtotal'])
        self.assertEqual(order_response.data['total'], params['total'])
        self.assertEqual(order_response.data['estimated_tax'], params['tax'])

    def test_order_discount_and_tax_calculation_with_multiple_promo_codes(self):
        """
        Test Order creation with various promo codes and products having 6 properties.
        We will test 6 different promo codes for the order with 6 different products.
        """

        # Test with different promo codes and different currencies
        for promo_code, expected_total in [
            (self.promo_20all.code, "$52.48"),  
            (self.promo_flat200.code, "$94.00"), 
            (self.promo_gold5.code, "$95.00"), 
            (self.promo_sell5.code, "$90.00"),  
            (self.promo_clearance20.code, "$80.00") 
        ]:
            if settings.BASE_CURRENCY == 'USD':
                self._create_order_with_promo(
                    promo_code=promo_code,
                    currency="USD",
                    params={
                        "subtotal": "$60.00",
                        "total": expected_total,
                        "tax": "$4.48",
                        "variant_1": {"price": 2.00, "cost_per_unit": 2.00, "stock": 10}, 
                        "variant_2": {"price": 3.00, "cost_per_unit": 4.00, "stock": 10},
                        "variant_3": {"price": 2.50, "cost_per_unit": 3.00, "stock": 10},
                        "variant_4": {"price": 3.50, "cost_per_unit": 2.00, "stock": 10}, 
                        "variant_5": {"price": 4.50, "cost_per_unit": 1.00, "stock": 10}, 
                        "variant_6": {"price": 1.50, "cost_per_unit": 1.00, "stock": 10}, 
                    }
                )

            if settings.BASE_CURRENCY == 'JPY':
                self._create_order_with_promo(
                    promo_code=promo_code,
                    currency="JPY",
                    params={
                        "subtotal": "¥11000",
                        "total": "¥8800",  
                        "tax": "¥1320",
                        "variant_1": {"price": 5000, "cost_per_unit": 4000, "stock": 10},
                        "variant_2": {"price": 3000, "cost_per_unit": 2500, "stock": 10}, 
                        "variant_3": {"price": 4550, "cost_per_unit": 3500, "stock": 10}, 
                        "variant_4": {"price": 6550, "cost_per_unit": 3500, "stock": 10}, 
                        "variant_5": {"price": 5550, "cost_per_unit": 3500, "stock": 10}, 
                        "variant_6": {"price": 4050, "cost_per_unit": 3500, "stock": 10}, 
                    }
                )

            if settings.BASE_CURRENCY == 'KWD':
                self._create_order_with_promo(
                    promo_code=promo_code,
                    currency="KWD",
                    params={
                        "subtotal": "KWD 60.00",
                        "total": "KWD 52.48",  
                        "tax": "KWD 4.48",
                        "variant_1": {"price": 2.00, "cost_per_unit": 2.00, "stock": 10}, 
                        "variant_2": {"price": 3.00, "cost_per_unit": 4.00, "stock": 10},
                        "variant_3": {"price": 2.50, "cost_per_unit": 3.00, "stock": 10},
                        "variant_4": {"price": 3.50, "cost_per_unit": 2.00, "stock": 10}, 
                        "variant_5": {"price": 4.50, "cost_per_unit": 1.00, "stock": 10}, 
                        "variant_6": {"price": 1.50, "cost_per_unit": 1.00, "stock": 10}, 
                    }
                )
