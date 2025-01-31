
from django.db import models

class PermissionsEnum(models.TextChoices):
    CAN_APPROVE_ORDER = "can_approve_order"
    CAN_CANCEL_ORDER = "can_cancel_order"
    CAN_SHIP_ORDER = "can_ship_order"
    CAN_PROCCSS_ORDER = "can_process_order"
    CAN_DELIVER_ORDER = "can_deliver_order"
    CAN_UPDATE_ORDER_PYMENT_TERM = "can_update_order_payment_term"
    CAN_UPDATE_ORDER_PAYMENT_METHOD = "can_update_order_payment_method"

    CAN_INITIATE_PAYMENT_REFUND = "CAN_INITIATE_PAYMENT_REFUND"

    CAN_BULK_PRODUCT_STATUS_UPDATE = "can_bulk_product_status_update"
    CAN_BULK_PRODUCT_DELETE = "can_bulk_product_delete"

    CAN_READ_CUSTOMER = "can_read_customer"
    CAN_UPDATE_CUSTOMER = "can_create_customer"