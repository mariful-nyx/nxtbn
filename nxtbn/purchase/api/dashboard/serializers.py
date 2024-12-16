from rest_framework import serializers
from nxtbn.purchase.models import PurchaseOrder
from nxtbn.users.api.dashboard.serializers import UserSerializer
from nxtbn.warehouse.api.dashboard.serializers import WarehouseSerializer
from nxtbn.product.api.dashboard.serializers import SupplierSerializer


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
        try:
            if obj.created_by and obj.created_by.first_name and obj.created_by.last_name:
                return f"{obj.created_by.first_name} {obj.created_by.last_name}"
            return None
        except AttributeError:
            # Return None if any attribute is missing or invalid
            return None
        

class PurchaseOrderDetailSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    destination = WarehouseSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = PurchaseOrder
        fields = [
            'id',
            'supplier',
            'destination',
            'status',
            'expected_delivery_date',
            'created_by',
            'total_cost'
        ]
