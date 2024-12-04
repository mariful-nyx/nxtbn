from rest_framework import serializers
from nxtbn.warehouse.models import Warehouse, Stock, StockMovement
from nxtbn.product.models import ProductVariant

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location']

class StockSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all()) 
    product_variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())

    class Meta:
        model = Stock
        fields = ['id', 'warehouse', 'product_variant', 'quantity']

class StockMovementSerializer(serializers.ModelSerializer):
    product_variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())
    from_warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    to_warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())

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
