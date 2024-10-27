from django.db import models
from django.utils.translation import gettext_lazy as _

class OrderAuthorizationStatus(models.TextChoices):
    """Defines the authorization status of an order based on fund coverage.

    - 'NONE': No funds are authorized.
    - 'PARTIAL': Partially authorized; authorized and charged funds do not fully cover the order's total after accounting for granted refunds.
    - 'FULL': Fully authorized; authorized and charged funds fully cover the order's total after accounting for granted refunds.
    """

    NONE = "NONE", "No funds are authorized"
    PARTIAL = "PARTIAL", "Partially authorized; funds don't fully cover the order's total"
    FULL = "FULL", "Fully authorized; funds cover the order's total"

class OrderChargeStatus(models.TextChoices):
    """Defines the charge status of an order based on transaction charges.

    - 'DUE': Payment is due; no funds have been charged yet.
    - 'PARTIAL': Partially charged; charged funds don't fully cover the order's total after accounting for granted refunds.
    - 'FULL': Fully charged; charged funds fully cover the order's total after accounting for granted refunds.
    - 'OVERCHARGED': Overcharged; charged funds exceed the order's total after accounting for granted refunds.
    """

    DUE = "DUE", _("Due")
    PARTIAL = "PARTIAL", _("Partially charged")
    FULL = "FULL", _("Fully charged")
    OVERCHARGED = "OVERCHARGED", _("Overcharged")


class OrderStatus(models.TextChoices):
    """Defines the different stages of an order's lifecycle.

    - 'PENDING': Order has been placed but not yet processed.
    - 'PROCESSING': Order is being processed and prepared for shipment.
    - 'SHIPPED': Order has been shipped but not yet delivered.
    - 'DELIVERED': Order has been delivered to the customer.
    - 'CANCELLED': Order has been cancelled and will not be fulfilled.
    - 'RETURNED': Order has been returned after delivery.
    """

    PENDING = "PENDING", _("Pending")
    APPROVED = "APPROVED", _("Approved")
    PROCESSING = "PROCESSING", _("Processing")
    SHIPPED = "SHIPPED", _("Shipped")
    DELIVERED = "DELIVERED", _("Delivered")
    CANCELLED = "CANCELLED", _("Cancelled")
    PENDING_RETURN = "PENDING_RETURN", _("Pending Return")
    RETURNED = "RETURNED", _("Returned")



class PaymentTerms(models.TextChoices): # incase of due payment
    """Defines the payment terms for an order based on when payment is due.

    - 'DUE_ON_RECEIPT': Payment is due upon receipt of the invoice.
    - 'DUE_ON_FULFILLMENT': Payment is due upon fulfillment of the order.
    - 'WITHIN_7_DAYS': Payment is due within 7 days.
    - 'WITHIN_15_DAYS': Payment is due within 15 days.
    - 'WITHIN_30_DAYS': Payment is due within 30 days.
    - 'WITHIN_45_DAYS': Payment is due within 45 days.
    - 'WITHIN_60_DAYS': Payment is due within 60 days.
    - 'WITHIN_90_DAYS': Payment is due within 90 days.
    - 'FIXED_DATE': Payment is due on a specific fixed date.
    """

    DUE_ON_RECEIPT = "DUE_ON_RECEIPT", "Due on receipt"
    DUE_ON_FULFILLMENT = "DUE_ON_FULFILLMENT", "Due on fulfillment"
    DUE_ON_INSTALLMENT = "DUE_ON_INSTALLMENT", "Due on installment"
    FIXED_DATE = "FIXED_DATE", "Fixed date"

    # below field will be used only in frontend to select payment terms
    """ 
    WITHIN_7_DAYS = "WITHIN_7_DAYS", "Within 7 days"
    WITHIN_15_DAYS = "WITHIN_15_DAYS", "Within 15 days"
    WITHIN_30_DAYS = "WITHIN_30_DAYS", "Within 30 days"
    WITHIN_45_DAYS = "WITHIN_45_DAYS", "Within 45 days"
    WITHIN_60_DAYS = "WITHIN_60_DAYS", "Within 60 days"
    WITHIN_90_DAYS = "WITHIN_90_DAYS", "Within 90 days"
    """


class AddressType(models.TextChoices):
    DSA = 'DSA', 'Default Shipping Address'
    DBA = 'DBA', 'Default Billing Address'
    SA = 'SA', 'Shipping Address'
    BA = 'BA', 'Billing Address'
    DSA_DBA = 'DSA_DBA', 'Default Shipping and Billing Address'


class ReturnStatus(models.TextChoices):
    REQUESTED = 'REQUESTED', _('Requested')
    APPROVED = 'APPROVED', _('Approved')
    REJECTED = 'REJECTED', _('Rejected')
    COMPLETED = 'COMPLETED', _('Completed')
    CANCELLED = 'CANCELLED', _('Cancelled')

