from rest_framework.views import APIView
from rest_framework import generics

from rest_framework.response import Response
from rest_framework import status

from nxtbn.order import AddressType
from nxtbn.order.models import Address
from nxtbn.product.models import ProductVariant
from decimal import Decimal

from nxtbn.shipping.models import ShippingRate


class OrderEstimateAPIView(generics.GenericAPIView):
    from nxtbn.core.api.common.serializers import OrderEstimateSerializer
    serializer_class = OrderEstimateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract data from validated serializer
        fixed_shipping_amount = serializer.validated_data.get('fixed_shipping_amount')
        variants_data = serializer.validated_data.get('variants')
        fixed_discount_amount = serializer.validated_data.get('fixed_discount_amount')

        # Retrieve variants from the database
        variants = []
        for variant_data in variants_data:
            try:
                variant = ProductVariant.objects.get(alias=variant_data['alias'])
                quantity = variant_data['quantity']
                variants.append({
                    'variant': variant,
                    'quantity': quantity,
                    'weight': variant.weight_value,
                    'price': variant.price
                })
            except ProductVariant.DoesNotExist:
                return Response({"error": "Variant not found."}, status=404)

        # Calculate total weight and total items based on variants
        total_weight = sum(variant['quantity'] * variant['weight'] for variant in variants)
        total_items = sum(variant['quantity'] for variant in variants)

        # Calculate subtotal from the variants
        total_subtotal = sum(variant['quantity'] * variant['price'] for variant in variants)

        # Calculate discount
        discount = self.calculate_discount(total_subtotal, fixed_discount_amount)
        discount_percentage = (discount / total_subtotal * 100) if total_subtotal > 0 else 0

        # Calculate shipping fee and name
        shipping_fee, shipping_name = self.calculate_shipping_fee(fixed_shipping_amount, total_weight)

        # Convert shipping_fee to Decimal
        shipping_fee = Decimal(shipping_fee)

        # Calculate estimated tax
        estimated_tax, tax_type, tax_percentage = self.calculate_tax(total_subtotal, discount)

        # Calculate total
        total = total_subtotal - discount + shipping_fee + estimated_tax

        response_data = {
            "subtotal": str(total_subtotal),
            "total_items": total_items,
            "discount": str(discount),
            "discount_percentage": discount_percentage,
            'discount_name': fixed_shipping_amount.get('name', '') if fixed_shipping_amount else '',
            "shipping_fee": str(shipping_fee),
            "shipping_name": shipping_name,
            "estimated_tax": str(estimated_tax),
            "tax_type": tax_type,
            "tax_percentage": str(tax_percentage * 100),
            "total": str(total),
        }

        return Response(response_data)

    def calculate_shipping_fee(self, fixed_shipping_amount, weight):
        shipping_fee = 0
        shipping_name = None

        if fixed_shipping_amount:
            shipping_fee = float(fixed_shipping_amount['price'])
            shipping_name = fixed_shipping_amount['name']

        return shipping_fee, shipping_name

    def calculate_discount(self, subtotal, fixed_discount_amount):
        """
        Calculate discount based on the fixed discount amount if provided.
        """
        discount = Decimal('0.00')  # Default no discount
        if fixed_discount_amount:
            discount = Decimal(fixed_discount_amount['price'])
        return discount

    def calculate_tax(self, subtotal, discount):
        tax_rate = Decimal('0.15')
        taxable_amount = subtotal - discount
        estimated_tax = taxable_amount * tax_rate
        tax_type = "VAT 15%"
        return estimated_tax, tax_type, tax_rate