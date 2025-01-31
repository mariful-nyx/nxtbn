
from django.db import models

class PermissionsEnum(models.TextChoices):
    CAN_APPROVE_ORDER = "can_approve_order"
    CAN_CANCEL_ORDER = "can_cancel_order"
    CAN_SHIP_ORDER = "can_ship_order"
    CAN_PROCCSS_ORDER = "can_process_order"
    CAN_DELIVER_ORDER = "can_deliver_order"