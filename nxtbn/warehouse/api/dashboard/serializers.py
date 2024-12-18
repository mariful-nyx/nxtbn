from rest_framework import serializers
from nxtbn.warehouse.models import StockReservation, Warehouse, Stock
from nxtbn.product.models import ProductVariant
from nxtbn.product.api.dashboard.serializers import ProductVariantSerializer


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all()) 
    product_variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())

    warehouse_name = serializers.SerializerMethodField()
    product_variant_name = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = [
            'id',
            'warehouse',
            'product_variant',
            'quantity',
            'warehouse_name',
            'product_variant_name',
            'reserved',
            'available_for_new_order',
        ]

    def get_warehouse_name(self, obj):
        return obj.warehouse.name
    
    def get_product_variant_name(self, obj):
        return obj.product_variant.name



class StockDetailViewSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'warehouse', 'product_variant', 'quantity', 'reserved', 'available_for_new_order',]


class StockUpdateSerializer(serializers.Serializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(), required=True)
    quantity = serializers.IntegerField(required=True)


class StockReservationSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)

    class Meta:
        model = StockReservation
        fields = [
            'id',
            'stock',
            'quantity',
            'purpose',
            'order_line',
        ]



class TransferStockReservationSerializer(serializers.ModelSerializer):
    destination = serializers.IntegerField(
        write_only=True, help_text="ID of the destination warehouse"
    )

    class Meta:
        model = StockReservation
        fields = ['id', 'stock', 'quantity', 'purpose', 'order_line', 'destination']
        read_only_fields = ['id', 'stock', 'quantity', 'purpose', 'order_line']

    def validate(self, data):
        """
        Perform validation of the destination warehouse, source stock,
        and ensure the reservation can be transferred.
        """
        reservation = self.instance
        destination_id = data.get('destination')

        # Validate destination warehouse
        try:
            destination_warehouse = Warehouse.objects.get(id=destination_id)
        except Warehouse.DoesNotExist:
            raise serializers.ValidationError({"destination": "Destination warehouse does not exist."})

        # Validate destination stock
        try:
            destination_stock = Stock.objects.get(
                warehouse=destination_warehouse,
                product_variant=reservation.stock.product_variant,
            )
        except Stock.DoesNotExist:
            raise serializers.ValidationError({
                "destination": "Destination stock does not exist."
            })

        # Check if destination has sufficient stock
        if destination_stock.quantity < reservation.quantity:
            raise serializers.ValidationError({
                "detail": (
                    "The destination warehouse does not have enough stock to accommodate the reservation. "
                    "Please transfer or add stock to the destination warehouse first."
                )
            })

        # Check if there's an existing reservation for the same order line
        destination_reservation = StockReservation.objects.filter(
            stock=destination_stock, order_line=reservation.order_line
        ).first()

        data['destination_stock'] = destination_stock
        data['destination_reservation'] = destination_reservation

        return data