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