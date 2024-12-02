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

    def __str__(self):
        return f"{self.product_variant.sku} in {self.warehouse.name}"



class StockMovement(AbstractBaseModel):
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
            self.from_warehouse = None  # No 'from_warehouse' for purchase
            self.to_warehouse = self.to_warehouse  # Ensure to_warehouse is set correctly for purchase
        elif self.movement_type == StockMovementType.SALE:
            self.to_warehouse = None  # No 'to_warehouse' for sale
        elif self.movement_type == StockMovementType.RETURN:
            self.to_warehouse = self.to_warehouse  # Ensure to_warehouse is set correctly for return
            self.from_warehouse = self.from_warehouse  # Ensure from_warehouse is set for return
        super().save(*args, **kwargs)
