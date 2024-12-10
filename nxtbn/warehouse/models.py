from django.db import models

from nxtbn.core.models import AbstractBaseModel
from nxtbn.product.models import ProductVariant
from nxtbn.warehouse import StockMovementType


class Warehouse(AbstractBaseModel):
    name = models.CharField(max_length=255, unique=True, help_text="Warehouse name. e.g. 'Main Warehouse' or 'Warehouse A' or 'store-1'")
    location = models.CharField(max_length=255)
    def __str__(self):
        return self.name

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



class StockMovement(AbstractBaseModel): # Stock movement is a record of the movement of stock from one warehouse to another.
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='stock_movements')
    from_warehouse = models.ForeignKey(Warehouse, related_name='outgoing_stock_movements', on_delete=models.CASCADE, null=True, blank=True)
    to_warehouse = models.ForeignKey(Warehouse, related_name='incoming_stock_movements', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    movement_type = models.CharField(max_length=20, choices=StockMovementType.choices)
    note = models.TextField(blank=True, null=True, help_text="Additional details about the movement.")

    def __str__(self):
        return f"{self.movement_type} for {self.product_variant.sku}"

    def save(self, *args, **kwargs):
        if self.movement_type == StockMovementType.PURCHASE:
            self.from_warehouse = None
            self.to_warehouse = self.to_warehouse 
        elif self.movement_type == StockMovementType.SALE:
            self.to_warehouse = None 
        elif self.movement_type == StockMovementType.RETURN:
            self.to_warehouse = self.to_warehouse
            self.from_warehouse = self.from_warehouse 
        super().save(*args, **kwargs)
