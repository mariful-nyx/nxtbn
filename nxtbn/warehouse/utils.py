
from nxtbn.order import OrderStockReservationStatus
from nxtbn.warehouse.models import Warehouse, Stock, StockReservation


from django.db import transaction
from django.core.exceptions import ValidationError

def reserve_stock(order):
    # Start a database transaction to ensure atomic operations
    with transaction.atomic():
        for item in order.line_items.all():
            required_quantity = item.quantity

            if item.variant.track_inventory:

                stocks = Stock.objects.filter(variant=item.variant).order_by('quantity')

                for stock in stocks:
                    if required_quantity <= 0:
                        break

                    if stock.quantity >= required_quantity:
                        # Deduct required quantity from the stock
                        stock.quantity -= required_quantity
                        stock.save()
                        StockReservation.objects.create(stock=stock, quantity=required_quantity, purpose="Pending Order")
                        order.reservation_status = OrderStockReservationStatus.RESERVED
                        required_quantity = 0
                    else:
                        # Partially deduct stock
                        required_quantity -= stock.quantity
                        stock.quantity = 0
                        stock.save()

                if required_quantity > 0:
                    # Raise error if stock is insufficient
                    order.reservation_status = OrderStockReservationStatus.FAILED
                    raise ValidationError(f"Insufficient stock for {item.variant.name}")
