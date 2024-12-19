from rest_framework import serializers
from nxtbn.purchase.models import PurchaseOrder, PurchaseOrderItem
from nxtbn.product.api.dashboard.serializers import SupplierSerializer, ProductVariantSerializer
from nxtbn.users.api.dashboard.serializers import UserSerializer
from nxtbn.warehouse.api.dashboard.serializers import WarehouseSerializer

class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.SerializerMethodField()
    destination_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    class Meta:
        model = PurchaseOrder
        fields = [
            'id',
            'supplier',
            'supplier_name',
            'destination',
            'destination_name',
            'status',
            'expected_delivery_date',
            'created_by',
            'created_by_name',
            'total_cost'
        ]
    def get_supplier_name(self, obj):
        return obj.supplier.name
    def get_destination_name(self, obj):
        return obj.destination.name
    def get_created_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"



class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = ['variant', 'ordered_quantity', 'unit_cost']

class PurchaseOrderCreateSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'destination', 'expected_delivery_date', 'items']

    def create(self, validated_data):
        request = self.context.get('request')
              
        items_data = validated_data.pop('items', [])

        if not items_data:
            raise serializers.ValidationError("Items are required")

       
        purchase_order = PurchaseOrder.objects.create(
            created_by=request.user,
            **validated_data
        )

        for item_data in items_data:
            PurchaseOrderItem.objects.create(purchase_order=purchase_order, **item_data)

        return purchase_order
    

class PurchaseOrderItemDetailSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    class Meta:
        model = PurchaseOrderItem
        fields = ['variant', 'ordered_quantity', 'unit_cost']


class PurchaseOrderDetailSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    destination = WarehouseSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    items = PurchaseOrderItemDetailSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            'id',
            'supplier',
            'destination',
            'status',
            'expected_delivery_date',
            'created_by',
            'total_cost',
            'items'
        ]