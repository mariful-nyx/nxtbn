from django.db import models

from nxtbn.core.models import AbstractBaseModel
from nxtbn.product.models import ProductVariant
from nxtbn.users.models import User
from nxtbn.warehouse import StockMovementStatus


class Warehouse(AbstractBaseModel):
    name = models.CharField(max_length=255, unique=True, help_text="Warehouse name. e.g. 'Main Warehouse' or 'Warehouse A' or 'store-1'")
    location = models.CharField(max_length=255)
    is_default = models.BooleanField(
        default=False,
        help_text="Only one warehouse can be default"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_default:
            Warehouse.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

class Stock(AbstractBaseModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="stocks")
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="warehouse_stocks")
    quantity = models.IntegerField(default=0)
    reserved = models.IntegerField(
        default=0,
        help_text=(
            "Quantity of this product variant that is reserved for specific purposes: "
            "1. Pending Orders: Items reserved for orders that have been placed but not yet fulfilled. "
            "2. Blocked Stock: Inventory set aside for quality control, specific customer allocation, or planned events. "
            "3. Pre-booked Stock: Stock promised to a customer or distributor but not yet shipped."
        )
    )

    def __str__(self):
        return f"{self.product_variant.sku} in {self.warehouse.name}"
    
    def available_for_new_order(self):
        return self.quantity - self.reserved



class StockReservation(AbstractBaseModel):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="reservations")
    quantity = models.PositiveIntegerField()
    purpose = models.CharField(max_length=50, help_text="Purpose of the reservation. e.g. 'Pending Order', 'Blocked Stock', 'Pre-booked Stock'")

    def __str__(self):
        return f"{self.quantity} reserved for {self.purpose}"

    def save(self, *args, **kwargs):
        if self.quantity > self.stock.quantity:
            raise ValueError("Reservation quantity cannot exceed stock quantity.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.stock.reserved -= self.quantity
        self.stock.save()
        super().delete(*args, **kwargs)

    def create(self, *args, **kwargs):
        self.stock.reserved += self.quantity
        self.stock.save()
        super().create(*args, **kwargs)



class StockTransfer(models.Model):
    """Tracks transfers of inventory between warehouses"""    
    from_warehouse = models.ForeignKey(Warehouse, related_name='transfers_out', on_delete=models.PROTECT)
    to_warehouse = models.ForeignKey(Warehouse, related_name='transfers_in', on_delete=models.PROTECT)
    
    status = models.CharField(max_length=20, choices=StockMovementStatus.choices, default=StockMovementStatus.PENDING)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Transfer {self.id} - {self.from_warehouse} to {self.to_warehouse}"

class StockTransferItem(models.Model):
    """Line items for a stock transfer"""
    stock_transfer = models.ForeignKey(StockTransfer, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"