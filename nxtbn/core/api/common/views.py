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
        self.validated_data = serializer.validated_data

        # Extract data from validated serializer
        variants_data = self.validated_data.get('variants')
        custom_discount_amount = self.validated_data.get('custom_discount_amount')
        shipping_method_id = self.validated_data.get('shipping_method_id', '')
        shipping_address = self.validated_data.get('shipping_address', {})

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
        discount = self.calculate_discount(total_subtotal, custom_discount_amount)
        discount_percentage = (discount / total_subtotal * 100) if total_subtotal > 0 else 0

        # Calculate shipping fee and name
        shipping_fee = self.get_total_shipping_fee(variants, shipping_method_id, shipping_address)
        shipping_name = self.validated_data.get('custom_shipping_amount', {}).get('name', '-')

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
            'discount_name': 'Discount Name',
            "shipping_fee": str(shipping_fee),
            "shipping_name": shipping_name,
            "estimated_tax": str(estimated_tax),
            "tax_type": tax_type,
            "tax_percentage": str(tax_percentage * 100),
            "total": str(total),
        }

        return Response(response_data)


    def calculate_discount(self, subtotal, custom_discount_amount):
        """
        Calculate discount based on the fixed discount amount if provided.
        """
        discount = Decimal('0.00')  # Default no discount
        if custom_discount_amount:
            discount = Decimal(custom_discount_amount['price'])
        return discount

    def calculate_tax(self, subtotal, discount):
        tax_rate = Decimal('0.15')
        taxable_amount = subtotal - discount
        estimated_tax = taxable_amount * tax_rate
        tax_type = "VAT 15%"
        return estimated_tax, tax_type, tax_rate
    
    def get_shipping_rate_instance(self, shipping_method_id, address):
        if not shipping_method_id:
            return None

        if not address:
            raise ValueError("Address is required as you request with shipping method id to get shipping rate instance.")

        shipping_rate_qs = ShippingRate.objects.filter(shipping_method__id=shipping_method_id)

        # Check for a rate defined at the city level
        if address.get('city', ''):
            rate = shipping_rate_qs.filter(city=address.get('city')).first()
            if rate:
                return rate

        # Check for a rate at the region/state level if no city rate is found
        if address.get('state', ''):
            rate = shipping_rate_qs.filter(region=address.get('state')).first()
            if rate:
                return rate

        # Check for a rate at the country level if no region rate is found
        if address.get('country', ''):
            rate = shipping_rate_qs.filter(country=address.get('country', '')).first()
            if rate:
                return rate

        # If no rate is found for the address, raise an exception
        raise ValueError("No shipping facility available for the provided location.")

    def get_shipping_fee_by_rate(self, shipping_method_id, address, total_weight):
        rate_instance = self.get_shipping_rate_instance(shipping_method_id, address)
        if not rate_instance:
            custom_shipping_amount = self.validated_data.get('custom_shipping_amount', {})
            if custom_shipping_amount:
                return custom_shipping_amount['price']
            else:
                return 0

        else:
            weight_min = rate_instance.weight_min
            weight_min = rate_instance.weight_min
            rate = rate_instance.rate
            shipping_fee = rate if total_weight <= weight_min else rate + (total_weight - weight_min) * rate
            return shipping_fee
        
    def get_total_shipping_fee(self, variants, shipping_method_id, address):
        total_weight = self.get_total_weight(variants)
        shipping_fee = self.get_shipping_fee_by_rate(shipping_method_id, address, total_weight)
        return shipping_fee
    
    def get_subtotal(self, variants):
        return sum(variant['quantity'] * variant['price'] for variant in variants)
    
    def get_total_items(self, variants):
        return sum(variant['quantity'] for variant in variants)
    
    def get_total_discount(self, subtotal, discount_amount):
        return discount_amount if discount_amount < subtotal else subtotal
    
    def get_total_cost(self, subtotal, discount, shipping_fee, tax):
        return subtotal - discount + shipping_fee + tax

    def get_total_weight(self, variants):
        return sum(variant['quantity'] * variant['weight'] for variant in variants)
    
