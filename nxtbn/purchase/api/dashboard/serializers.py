from rest_framework import serializers
from nxtbn.purchase import PurchaseStatus
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
            status=PurchaseStatus.DRAFT,
            **validated_data
        )

        for item_data in items_data:
            PurchaseOrderItem.objects.create(purchase_order=purchase_order, **item_data)

        return purchase_order
    

class PurchaseOrderItemDetailSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    class Meta:
        model = PurchaseOrderItem
        fields = ['variant', 'ordered_quantity', 'received_quantity', 'rejected_quantity', 'unit_cost']


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


class PurchaseOrderItemUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    received_quantity = serializers.IntegerField()
    rejected_quantity = serializers.IntegerField()

    def validate(self, data):
        item_id = data['id']
        received_quantity = data['received_quantity']
        rejected_quantity = data['rejected_quantity']

    
        instance = self.context.get('instance')

        try:
            order_item = instance.items.get(id=item_id)
        except PurchaseOrderItem.DoesNotExist:
            raise serializers.ValidationError(
                f"Item with id {item_id} does not exist in the purchase order."
            )

        if received_quantity > order_item.ordered_quantity:
            raise serializers.ValidationError(
                f"Received quantity ({received_quantity}) cannot exceed ordered quantity ({order_item.ordered_quantity})."
            )

        if received_quantity < order_item.received_quantity:
            raise serializers.ValidationError(
                f"Received quantity ({received_quantity}) cannot be less than the current received quantity ({order_item.received_quantity})."
            )

        adjusted_quantity = order_item.ordered_quantity - received_quantity
        if rejected_quantity > adjusted_quantity:
            raise serializers.ValidationError(
                f"Rejected quantity ({rejected_quantity}) cannot exceed the adjusted quantity ({adjusted_quantity})."
            )

        return data



class InventoryReceivingSerializer(serializers.Serializer):
    items = PurchaseOrderItemUpdateSerializer(many=True)
