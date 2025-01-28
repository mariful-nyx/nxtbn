

import graphene

from nxtbn.core.admin_permissions import check_user_permissions
from nxtbn.warehouse.admin_types import StockReservationType, StockTransferItemType, StockTransferType, StockType, WarehouseType
from nxtbn.warehouse.models import Stock, StockReservation, StockTransfer, StockTransferItem, Warehouse
from graphene_django.filter import DjangoFilterConnectionField



class WarehouseQuery(graphene.ObjectType):
    warehouses = DjangoFilterConnectionField(WarehouseType)
    stocks = DjangoFilterConnectionField(StockType)
    stock_reservations = DjangoFilterConnectionField(StockReservationType)
    stock_transfers = DjangoFilterConnectionField(StockTransferType)
    stock_transfer_items = DjangoFilterConnectionField(StockTransferItemType)
    
    warehouse = graphene.Field(WarehouseType, id=graphene.ID(required=True))
    stock = graphene.Field(StockType, id=graphene.ID(required=True))
    stock_reservation = graphene.Field(StockReservationType, id=graphene.ID(required=True))
    stock_transfer = graphene.Field(StockTransferType, id=graphene.ID(required=True))
    stock_transfer_item = graphene.Field(StockTransferItemType, id=graphene.ID(required=True))

    def resolve_warehouses(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return Warehouse.objects.all()

    def resolve_stocks(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return Stock.objects.all()

    def resolve_stock_reservations(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return StockReservation.objects.all()

    def resolve_stock_transfers(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return StockTransfer.objects.all()

    def resolve_stock_transfer_items(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return StockTransferItem.objects.all()

    def resolve_warehouse(root, info, id):
        check_user_permissions(info, any_staff=True)
        try:
            return Warehouse.objects.get(pk=id)
        except Warehouse.DoesNotExist:
            return None

    def resolve_stock(root, info, id):
        check_user_permissions(info, any_staff=True)
        try:
            return Stock.objects.get(pk=id)
        except Stock.DoesNotExist:
            return None

    def resolve_stock_reservation(root, info, id):
        check_user_permissions(info, any_staff=True)
        try:
            return StockReservation.objects.get(pk=id)
        except StockReservation.DoesNotExist:
            return None

    def resolve_stock_transfer(root, info, id):
        check_user_permissions(info, any_staff=True)
        try:
            return StockTransfer.objects.get(pk=id)
        except StockTransfer.DoesNotExist:
            return None

    def resolve_stock_transfer_item(root, info, id):
        check_user_permissions(info, any_staff=True)
        try:
            return StockTransferItem.objects.get(pk=id)
        except StockTransferItem.DoesNotExist:
            return None
