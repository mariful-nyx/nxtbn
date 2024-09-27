from rest_framework import generics

from rest_framework.response import Response
from rest_framework import status

from nxtbn.product.models import ProductVariant
from decimal import Decimal

from nxtbn.shipping.models import ShippingRate
from nxtbn.tax.models import TaxRate

from django.db.models import Q
from rest_framework import serializers


class OrderEstimateAPIView(generics.GenericAPIView):
    from nxtbn.core.api.common.serializers import OrderEstimateSerializer
    serializer_class = OrderEstimateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validated_data = serializer.validated_data

        try:
            # Extract data from validated serializer
            variants_data = self.validated_data.get('variants')
            custom_discount_amount = self.validated_data.get('custom_discount_amount')
            shipping_method_id = self.validated_data.get('shipping_method_id', '')
            shipping_address = self.validated_data.get('shipping_address', {})

            # Retrieve variants from the database
            variants = self.get_variants()

            # Calculate subtotal from the variants
            total_subtotal = self.get_subtotal(variants)

            # Calculate discount
            discount = self.calculate_discount(total_subtotal, custom_discount_amount)
            discount_percentage = (discount / total_subtotal * 100) if total_subtotal > 0 else 0

            # Calculate shipping fee and name
            shipping_fee, shipping_name = self.get_total_shipping_fee(variants, shipping_method_id, shipping_address)

            # Convert shipping_fee to Decimal
            shipping_fee = Decimal(shipping_fee)

            # Calculate estimated tax
            estimated_tax, tax_details = self.calculate_tax(variants, discount, shipping_address)

            # Calculate total
            total = total_subtotal - discount + shipping_fee + estimated_tax

            response_data = {
                "subtotal": str(total_subtotal),
                "total_items": self.get_total_items(variants),
                "discount": str(discount),
                "discount_percentage": discount_percentage,
                'discount_name': 'Discount Name',  # You might want to make this dynamic
                "shipping_fee": str(shipping_fee),
                "shipping_name": shipping_name,
                "estimated_tax": str(estimated_tax),
                "tax_details": tax_details,  # Detailed tax information
                "total": str(total),
            }

            return Response(response_data)

        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_variants(self):
        variants_data = self.validated_data.get('variants')
        variants = []
        for variant_data in variants_data:
            try:
                variant = ProductVariant.objects.get(alias=variant_data['alias'])
                quantity = variant_data['quantity']
                weight = variant.weight_value if variant.weight_value is not None else Decimal('0.00')
                variants.append({
                    'variant': variant,
                    'quantity': quantity,
                    'weight': weight,
                    'price': variant.price,
                    'tax_class': variant.product.tax_class,
                })
            except ProductVariant.DoesNotExist:
                raise serializers.ValidationError({"variants": f"Variant with alias '{variant_data['alias']}' not found."})
        return variants

    def calculate_discount(self, subtotal, custom_discount_amount):
        """
        Calculate discount based on the fixed discount amount if provided.
        """
        discount = Decimal('0.00')  # Default no discount
        if custom_discount_amount:
            discount = Decimal(custom_discount_amount['price'])
        # Ensure discount does not exceed subtotal
        return min(discount, subtotal)

    def calculate_tax(self, variants, discount, shipping_address):
        """
        Calculate tax based on each product's tax_class and the applicable TaxRate.
        Hierarchy for TaxRate: State > Country
        """
        from collections import defaultdict

        # Group subtotal by tax_class
        tax_class_subtotals = defaultdict(Decimal)
        for variant in variants:
            tax_class = variant['tax_class']
            variant_subtotal = variant['quantity'] * variant['price']
            tax_class_subtotals[tax_class] += variant_subtotal

        # Calculate total subtotal for proportional discount allocation
        total_subtotal = sum(tax_class_subtotals.values())
        if total_subtotal > 0 and discount > 0:
            for tax_class in tax_class_subtotals:
                # Allocate discount proportionally based on subtotal
                tax_class_subtotals[tax_class] -= (tax_class_subtotals[tax_class] / total_subtotal) * discount

        estimated_tax = Decimal('0.00')
        tax_details = []

        for tax_class, class_subtotal in tax_class_subtotals.items():
            tax_rate_instance = self.get_tax_rate(tax_class, shipping_address)
            if tax_rate_instance:
                tax_rate = tax_rate_instance.rate / Decimal('100')  # Assuming rate is percentage
                tax_type = tax_rate_instance.tax_class.name  # Assuming you want the tax class name
            else:
                tax_rate = Decimal('0.00')
                tax_type = 'No Tax'

            class_tax = (class_subtotal * tax_rate).quantize(Decimal('0.01'))
            estimated_tax += class_tax

            tax_details.append({
                'tax_class': tax_type,
                'tax_percentage': str(tax_rate * 100),
                'tax_amount': str(class_tax),
            })

        return estimated_tax, tax_details

    def get_tax_rate(self, tax_class, shipping_address):
        """
        Retrieve the applicable TaxRate for a given tax_class and shipping_address.
        Hierarchy: State > Country
        """
        tax_rate_instance = None

        if 'state' in shipping_address and shipping_address['state']:
            tax_rate_instance = TaxRate.objects.filter(
                tax_class=tax_class,
                state=shipping_address['state'],
                is_active=True
            ).first()

        if not tax_rate_instance and 'country' in shipping_address and shipping_address['country']:
            tax_rate_instance = TaxRate.objects.filter(
                tax_class=tax_class,
                country=shipping_address['country'],
                is_active=True
            ).first()

        return tax_rate_instance

    def get_shipping_rate_instance(self, shipping_method_id, address):
        if not shipping_method_id:
            return None

        if not address:
            raise ValueError("Address is required when a shipping method ID is provided.")

        shipping_rate_qs = ShippingRate.objects.filter(shipping_method__id=shipping_method_id)

        # Check for a rate defined at the state level
        if address.get('state'):
            rate = shipping_rate_qs.filter(state=address['state']).first()
            if rate:
                return rate

        # Check for a rate at the country level if no state rate is found
        if address.get('country'):
            rate = shipping_rate_qs.filter(country=address['country']).first()
            if rate:
                return rate

        # If no rate is found for the address, raise an exception
        raise ValueError("No shipping rate available for the provided location.")

    def get_shipping_fee_by_rate(self, shipping_method_id, address, total_weight):
        rate_instance = self.get_shipping_rate_instance(shipping_method_id, address)
        if not rate_instance:
            custom_shipping_amount = self.validated_data.get('custom_shipping_amount', {})
            if custom_shipping_amount:
                return Decimal(custom_shipping_amount['price']), custom_shipping_amount.get('name', '-')
            else:
                return Decimal('0.00'), '-'

        # Calculate shipping fee based on weight
        base_weight = rate_instance.weight_min
        base_rate = rate_instance.rate
        incremental_rate = rate_instance.incremental_rate  # Assume ShippingRate has incremental_rate field

        if total_weight <= base_weight:
            shipping_fee = base_rate
        else:
            extra_weight = total_weight - base_weight
            shipping_fee = base_rate + (extra_weight * incremental_rate)

        shipping_name = rate_instance.name if hasattr(rate_instance, 'name') else 'Standard Shipping'

        return shipping_fee, shipping_name

    def get_total_shipping_fee(self, variants, shipping_method_id, address):
        total_weight = self.get_total_weight(variants)
        shipping_fee, shipping_name = self.get_shipping_fee_by_rate(shipping_method_id, address, total_weight)
        return shipping_fee, shipping_name

    def get_subtotal(self, variants):
        return sum(variant['quantity'] * variant['price'] for variant in variants)

    def get_total_items(self, variants):
        return sum(variant['quantity'] for variant in variants)

    def get_total_weight(self, variants):
        return sum(variant['quantity'] * variant['weight'] for variant in variants)
