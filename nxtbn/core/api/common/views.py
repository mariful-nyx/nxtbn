from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from nxtbn.product.models import ProductVariant
from decimal import Decimal


class OrderEstimateAPIView(APIView):

    def post(self, request):
        from nxtbn.core.api.common.serializers import OrderEstimateSerializer
        serializer = OrderEstimateSerializer(data=request.data)
        if serializer.is_valid():
            total_subtotal = Decimal('0.00')
            total_items = 0
            discount = Decimal('0.00')  # Add your actual discount logic here
            discount_percentage = 0.0  # If discount is percentage based, you can calculate it

            # Get shipping details if provided
            fixed_shipping_amount = serializer.validated_data.get('fixed_shipping_amount', None)
            shipping_fee = Decimal(fixed_shipping_amount['price']) if fixed_shipping_amount else Decimal('0.00')
            shipping_name = fixed_shipping_amount['name'] if fixed_shipping_amount else None

            tax_percentage = Decimal('0.15')  # Assuming a 15% VAT
            tax_type = "VAT 15%"  # Modify as needed

            # Iterate through variants to calculate subtotal and total items
            for item in serializer.validated_data['variants']:
                try:
                    variant = ProductVariant.objects.get(alias=item['alias'])
                    quantity = item['quantity']
                    total_items += quantity
                    total_subtotal += variant.price * quantity
                except ProductVariant.DoesNotExist:
                    return Response({"error": f"Variant with alias {item['alias']} not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Example tax calculation based on subtotal
            estimated_tax = total_subtotal * tax_percentage

            # Final total calculation
            total = total_subtotal - discount + estimated_tax + shipping_fee

            # Prepare the response data with only the requested fields
            response_data = {
                "subtotal": str(total_subtotal),         # Total price of items
                "total_items": total_items,              # Total quantity of items
                "discount": str(discount),               # Amount of discount
                "discount_percentage": discount_percentage,  # Percentage discount if applicable
                "shipping_fee": str(shipping_fee),       # Amount of shipping fee
                "shipping_name": shipping_name,          # Shipping name (if provided)
                "estimated_tax": str(estimated_tax),     # Tax amount
                "tax_type": tax_type,                    # Tax type (e.g., VAT 15%)
                "tax_percentage": str(tax_percentage * 100),  # Tax percentage in string format
                "total": str(total),                    # Final total amount
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)