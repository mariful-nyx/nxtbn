from rest_framework import serializers
from nxtbn.purchase.models import PurchaseOrder


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

