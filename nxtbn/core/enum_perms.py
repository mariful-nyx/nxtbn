
from django.db import models

class PermissionsEnum(models.TextChoices):
    CAN_APPROVE_ORDER = "can_approve_order"
    CAN_CANCEL_ORDER = "can_cancel_order"
    CAN_SHIP_ORDER = "can_ship_order"