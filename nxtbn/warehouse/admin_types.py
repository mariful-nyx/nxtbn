import graphene
from graphene_django.types import DjangoObjectType
from graphene import relay
from nxtbn.warehouse.models import (
    Warehouse,
    Stock,
    StockReservation,
    StockTransfer,
    StockTransferItem,
)

class WarehouseType(DjangoObjectType):
    class Meta:
        model = Warehouse
        fields = "__all__"  
        interfaces = (relay.Node,)
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
        }

class StockType(DjangoObjectType):
    class Meta:
        model = Stock
        fields = "__all__"
        interfaces = (relay.Node,)
        filter_fields = {
            "warehouse": ["exact"],
            "product_variant": ["exact"],
        }

class StockReservationType(DjangoObjectType):
    class Meta:
        model = StockReservation
        fields = "__all__"
        interfaces = (relay.Node,)
        filter_fields = {
            "stock": ["exact"],
            "purpose": ["exact", "icontains", "istartswith"],
        }

class StockTransferType(DjangoObjectType):
    class Meta:
        model = StockTransfer
        fields = "__all__"
        interfaces = (relay.Node,)
        filter_fields = {
            "from_warehouse": ["exact"],
            "to_warehouse": ["exact"],
            "status": ["exact"],
        }

class StockTransferItemType(DjangoObjectType):
    class Meta:
        model = StockTransferItem
        fields = "__all__"
        interfaces = (relay.Node,)
        filter_fields = {
            "stock_transfer": ["exact"],
            "variant": ["exact"],
        }