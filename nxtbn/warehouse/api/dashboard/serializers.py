from rest_framework import serializers
from nxtbn.warehouse.models import Warehouse, Stock, StockMovement

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location']

class StockSerializer(serializers.ModelSerializer):
    warehouse = serializers.StringRelatedField() 
    product_variant = serializers.StringRelatedField()

    class Meta:
        model = Stock
        fields = ['id', 'warehouse', 'product_variant', 'quantity']

class StockMovementSerializer(serializers.ModelSerializer):
    product_variant = serializers.StringRelatedField()
    from_warehouse = serializers.StringRelatedField()
    to_warehouse = serializers.StringRelatedField()

    class Meta:
        model = StockMovement
        fields = [
            'id',
            'product_variant',
            'from_warehouse',
            'to_warehouse',
            'quantity',
            'movement_type',
            'note',
        ]
