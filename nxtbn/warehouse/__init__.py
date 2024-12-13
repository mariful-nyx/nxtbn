from django.db import models

class StockMovementType(models.TextChoices):
    PURCHASE = 'PURCHASE', 'Purchase'
    TRANSFER_IN = 'TRANSFER_IN', 'Transfer In'
    TRANSFER_OUT = 'TRANSFER_OUT', 'Transfer Out'
    SALE = 'SALE', 'Sale'
    RETURN = 'RETURN', 'Return'


class StockMovementStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    IN_TRANSIT = 'IN_TRANSIT', 'In Transit'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'
