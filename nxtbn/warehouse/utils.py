from nxtbn.order import OrderStockReservationStatus
from nxtbn.warehouse.models import Warehouse, Stock, StockReservation

from django.db import transaction
from django.core.exceptions import ValidationError

def adjust_stock(stock, reserved_delta, quantity_delta):
    """
    Adjust stock's reserved and quantity fields atomically.

    Args:
        stock: The stock instance to adjust.
        reserved_delta: Change in reserved quantity (+/-).
        quantity_delta: Change in available quantity (+/-).

    Raises:
        ValidationError: If adjustments would result in negative values for reserved or quantity.
    """
    if stock.quantity + quantity_delta < 0:
        raise ValidationError("Insufficient stock to adjust quantity.")
    if stock.reserved + reserved_delta < 0:
        raise ValidationError("Reserved stock cannot be negative.")

    stock.reserved += reserved_delta
    stock.quantity += quantity_delta
    stock.save()

def reserve_stock(order):
    """
    Reserve stock for the given order by deducting available stock from warehouses.
    If stock is insufficient for any item, the operation will rollback and raise a ValidationError.
    """
    with transaction.atomic():
        for item in order.line_items.all():
            required_quantity = item.quantity

            if item.variant.track_inventory:
                # Fetch stocks for the product variant ordered by available quantity
                stocks = Stock.objects.filter(
                    product_variant=item.variant
                ).order_by('quantity')

                for stock in stocks:
                    if required_quantity <= 0:
                        break

                    available_quantity = stock.quantity - stock.reserved
                    if available_quantity <= 0:
                        continue

                    if available_quantity >= required_quantity:
                        # Deduct the required quantity and reserve it
                        adjust_stock(stock, reserved_delta=required_quantity, quantity_delta=0)

                        StockReservation.objects.create(
                            stock=stock,
                            quantity=required_quantity,
                            purpose="Pending Order",
                            order_line=item
                        )

                        order.reservation_status = OrderStockReservationStatus.RESERVED
                        required_quantity = 0
                    else:
                        # Partially reserve stock and continue with the remaining quantity
                        adjust_stock(stock, reserved_delta=available_quantity, quantity_delta=0)

                        StockReservation.objects.create(
                            stock=stock,
                            quantity=available_quantity,
                            purpose="Pending Order",
                            order_line=item
                        )

                        required_quantity -= available_quantity

                if required_quantity > 0:
                    # If we couldn't reserve the full quantity, rollback and raise an error
                    order.reservation_status = OrderStockReservationStatus.FAILED
                    raise ValidationError(f"Insufficient stock for {item.variant.name}")

        # Save the order's reservation status after successful reservation
        order.save()

def release_stock(order):
    """
    Release reserved stock for an order and restore the quantities to available stock.

    Args:
        order: The order instance whose stock reservations are to be released.

    Returns:
        The updated order instance with the reservation status set to `RELEASED`.

    Side Effects:
        - Restores stock quantities in the `Stock` model.
        - Deletes `StockReservation` entries.
        - Updates the order's reservation status to `RELEASED`.
    """
    with transaction.atomic():
        for item in order.line_items.all():
            if item.variant.track_inventory:
                for reservation in item.reservations.all():
                    stock = reservation.stock
                    adjust_stock(stock, reserved_delta=-reservation.quantity, quantity_delta=0)
                    reservation.delete()

        order.reservation_status = OrderStockReservationStatus.RELEASED
        order.save()
        return order

def deduct_reservation_on_dispatch(order):
    with transaction.atomic():
        for item in order.line_items.all():
            if item.variant.track_inventory:
                # Use the correct related name for accessing reservations
                for reservation in item.stock_reservations.all():
                    stock = reservation.stock

                    if stock.reserved < reservation.quantity:
                        raise ValidationError(
                            f"Reservation quantity for {item.variant.name} exceeds available reserved stock."
                        )

                    # Deduct reserved quantity permanently
                    adjust_stock(stock, reserved_delta=-reservation.quantity, quantity_delta=-reservation.quantity)

                    # Remove the reservation
                    reservation.delete()

        order.reservation_status = OrderStockReservationStatus.SHIPPED
        order.save()
        return order