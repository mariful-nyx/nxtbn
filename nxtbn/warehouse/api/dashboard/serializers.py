from rest_framework import serializers
from nxtbn.warehouse.models import Warehouse, Stock, StockMovement
from nxtbn.product.models import ProductVariant
from nxtbn.product.api.dashboard.serializers import ProductVariantSerializer


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location']

class StockSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all()) 
    product_variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())

    warehouse_name = serializers.SerializerMethodField()
    product_variant_name = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = ['id', 'warehouse', 'product_variant', 'quantity', 'warehouse_name', 'product_variant_name']

    def get_warehouse_name(self, obj):
        return obj.warehouse.name
    
    def get_product_variant_name(self, obj):
        return obj.product_variant.name



class StockDetailViewSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'warehouse', 'product_variant', 'quantity']



class StockMovementSerializer(serializers.ModelSerializer):
    product_variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())
    from_warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    to_warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())

    product_variant_name = serializers.SerializerMethodField()
    from_warehouse_name = serializers.SerializerMethodField()
    to_warehouse_name = serializers.SerializerMethodField()

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
            'product_variant_name',
            'from_warehouse_name',
            'to_warehouse_name'

        ]

    def get_product_variant_name(self, obj):
        return obj.product_variant.name if obj.product_variant else None

    def get_from_warehouse_name(self, obj):
        return obj.from_warehouse.name if obj.from_warehouse else None

    def get_to_warehouse_name(self, obj):
        return obj.to_warehouse.name if obj.to_warehouse else None
    


class StockMovementDetailSerializer(serializers.ModelSerializer):
    
    product_variant = ProductVariantSerializer(read_only=True)
    from_warehouse = WarehouseSerializer(read_only=True)
    to_warehouse = WarehouseSerializer(read_only=True)

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