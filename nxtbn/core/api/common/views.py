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
        shipping_address = serializer.validated_data.get('shipping_address')
        customer_id = serializer.validated_data.get('customer_id')
        fixed_shipping_amount = serializer.validated_data.get('fixed_shipping_amount')
        variants_data = serializer.validated_data.get('variants')

        # Retrieve variants from the database
        variants = []
        for variant_data in variants_data:
            try:
                variant = ProductVariant.objects.get(alias=variant_data['alias'])
                quantity = variant_data['quantity']
                variants.append({
                    'variant': variant,
                    'quantity': quantity,
                    'weight': variant.weight_value,  # Assuming weight_value is in the ProductVariant model
                    'price': variant.price  # Assuming price is in the ProductVariant model
                })
            except ProductVariant.DoesNotExist:
                return Response({"error": "Variant not found."}, status=404)

        # Calculate total weight and total items based on variants
        total_weight = sum(variant['quantity'] * variant['weight'] for variant in variants)
        total_items = sum(variant['quantity'] for variant in variants)

        # Calculate subtotal from the variants
        total_subtotal = sum(variant['quantity'] * variant['price'] for variant in variants)

        # Calculate discount
        discount = self.calculate_discount(total_subtotal)
        discount_percentage = (discount / total_subtotal) * 100 if total_subtotal > 0 else 0

        # Calculate shipping fee and name
        shipping_fee, shipping_name = self.calculate_shipping_fee(shipping_address, customer_id, fixed_shipping_amount, total_weight)
        # Convert shipping_fee to Decimal
        shipping_fee = Decimal(shipping_fee)

        # Calculate estimated tax
        estimated_tax, tax_type, tax_percentage = self.calculate_tax(total_subtotal, discount)

        # Calculate total
        total = total_subtotal - discount + shipping_fee + estimated_tax

        print(total_subtotal, discount, shipping_fee, estimated_tax)

        response_data = {
            "subtotal": str(total_subtotal),                  # Total price of items
            "total_items": total_items,                        # Total quantity of items
            "discount": str(discount),                         # Amount of discount
            "discount_percentage": discount_percentage,        # Percentage discount if applicable
            "shipping_fee": str(shipping_fee),                # Amount of shipping fee
            "shipping_name": shipping_name,                    # Shipping name (if provided)
            "estimated_tax": str(estimated_tax),              # Tax amount
            "tax_type": tax_type,                              # Tax type (e.g., VAT 15%)
            "tax_percentage": str(tax_percentage * 100),      # Tax percentage in string format
            "total": str(total),                               # Final total amount
        }

        return Response(response_data)

    def calculate_shipping_fee(self, shipping_address, customer_id, fixed_shipping_amount, weight):
        """
        Calculate the shipping fee based on the address and weight.
        """
        shipping_fee = 0
        shipping_name = None

        if shipping_address:
            # Use the shipping address to find applicable rates
            shipping_fee, shipping_name = self.get_shipping_rate(shipping_address, weight)
        elif customer_id:
            # Retrieve the customer's default shipping address
            customer_address = Address.objects.filter(user__id=customer_id, address_type=AddressType.DSA).first()
            if customer_address:
                shipping_fee, shipping_name = self.get_shipping_rate(customer_address, weight)
        elif fixed_shipping_amount:
            # Use the fixed shipping amount if applicable
            shipping_fee = float(fixed_shipping_amount['price'])  # Assuming price is a string that needs conversion
            shipping_name = fixed_shipping_amount['name']

        print(shipping_fee, shipping_name)
        return shipping_fee, shipping_name

    def get_shipping_rate(self, address, weight):
        """
        Retrieve shipping rates based on address and weight.
        """
        shipping_rates = ShippingRate.objects.filter(
            country=address.country,
            weight_min__lte=weight,
            weight_max__gte=weight
        )

        if shipping_rates.exists():
            lowest_rate = shipping_rates.order_by('rate').first()
            return lowest_rate.rate, lowest_rate.shipping_method.name

        return 0, None  # Default to zero if no rates found

    def calculate_discount(self, subtotal):
        """
        Placeholder function to calculate discount.
        """
        # Implement your discount logic here
        discount = 0  # Assume no discount for now
        return discount

    def calculate_tax(self, subtotal, discount):
        """
        Calculate estimated tax based on subtotal and discount.
        """
        tax_rate = Decimal('0.15')  # Use Decimal for the tax rate
        taxable_amount = subtotal - discount
        estimated_tax = taxable_amount * tax_rate
        tax_type = "VAT 15%"  # Example tax type
        return estimated_tax, tax_type, tax_rate