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
            fixed_shipping_amount = serializer.validated_data.get('fixed_shipping_amount', None)
            shipping_fee = Decimal(fixed_shipping_amount['price']) if fixed_shipping_amount else Decimal('0.00')
            estimated_tax = Decimal('0.00')  # Adjust based on your tax calculation logic
            tax_type = "VAT 15%"  # Modify as needed
            
            for item in serializer.validated_data['variants']:
                try:
                    variant = ProductVariant.objects.get(alias=item['alias'])
                    quantity = item['quantity']
                    total_items += quantity
                    total_subtotal += variant.price * quantity
                except ProductVariant.DoesNotExist:
                    return Response({"error": f"Variant with alias {item['alias']} not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Example tax calculation based on subtotal
            estimated_tax = total_subtotal * Decimal('0.15')  # Assuming a 15% VAT

            total_after_discount = total_subtotal - discount
            total_after_tax = total_after_discount + estimated_tax
            total = total_after_tax + shipping_fee

            response_data = {
                "subtotal": str(total_subtotal),
                "total_items": total_items,
                "discount": str(discount),
                "total_after_discount": str(total_after_discount),
                "shipping_fee": str(shipping_fee),
                "estimated_tax": str(estimated_tax),
                "total_after_tax": str(total_after_tax),
                "tax_type": tax_type,
                "total": str(total),
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)