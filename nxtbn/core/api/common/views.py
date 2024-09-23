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
            discount = Decimal('0.00')  # Adjust this if you have discount logic
            shipping_fee = Decimal('10.00')  # Example static shipping fee
            estimated_tax = Decimal('0.00')  # Adjust this based on tax calculation logic
            tax_type = "Standard"  # Change as needed
            
            for item in serializer.validated_data['variants']:
                try:
                    variant = ProductVariant.objects.get(alias=item['alias'])
                    quantity = item['quantity']
                    total_items += quantity
                    total_subtotal += variant.price * quantity
                except ProductVariant.DoesNotExist:
                    return Response({"error": f"Variant with alias {item['alias']} not found."}, status=status.HTTP_400_BAD_REQUEST)

            total = total_subtotal - discount + shipping_fee + estimated_tax
            
            response_data = {
                "subtotal": str(total_subtotal),
                "total_items": total_items,
                "discount": str(discount),
                "shipping_fee": str(shipping_fee),
                "estimated_tax": str(estimated_tax),
                "tax_type": tax_type,
                "total": str(total),
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
