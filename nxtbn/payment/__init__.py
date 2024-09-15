from django.db import models
from django.utils.translation import gettext_lazy as _

class PaymentStatus(models.TextChoices):
    """Defines the different statuses of a payment process.

    - 'AUTHORIZED': Payment has been initiated but not yet completed. authorized means it is still pending
    - 'CAPTURED': Captured has been successfully completed. captured means the payment has be completed
    - 'FAILED': Payment attempt has failed or was unsuccessful.
    - 'REFUNDED': Payment has been refunded to the customer.
    - 'CANCELED': Payment has been canceled before completion.
    """

    AUTHORIZED = "AUTHORIZED", _("Authorized")
    CAPTURED = "CAPTURED", _("Captured")
    FAILED = "FAILED", _("Failed")
    REFUNDED = "REFUNDED", _("Refunded")
    CANCELED = "CANCELED", _("Canceled")



class PaymentMethod(models.TextChoices):
    """
    Defines different methods for processing payments. Each method represents
    a specific way for a customer to complete a transaction.

    Available options:
    
    - 'CREDIT_CARD': Payment via credit card.
    - 'PAYPAL': Payment through PayPal.
    - 'BANK_TRANSFER': Payment via bank transfer.
    - 'CASH_ON_DELIVERY': Payment upon delivery.
    - 'GIFT_CARD': Payment via a gift card.
    - 'DIRECT_DEBIT': Payment through direct debit from a bank account.
    - 'CASH_IN_STORE': Payment made in-store.
    - 'MFS': Payment through Mobile Financial Services (MFS) like mobile wallets or mobile banking.
    - 'CARRIER_BILLING': Payment through carrier billing, where charges are added to the customer's mobile phone bill.
    - 'CRYPTOCURRENCY': Payment using digital currencies such as Bitcoin or Ethereum.
    - 'BUY_NOW_PAY_LATER': Payment through services that allow purchases with deferred payments.
    - 'E_WALLET': Payment using electronic wallets like Skrill or Neteller.
    - 'BANK_TRANSFER_INSTANT': Instant bank transfer through networks like SEPA Instant Credit Transfer or Faster Payments.
    - 'POSTAL_MONEY_ORDER': Payment using postal money orders.
    - 'CHEQUE': Payment made with a cheque.
    - 'OTHER': Any other form of payment that doesn't fall into the predefined categories.
    """

    CREDIT_CARD = "CREDIT_CARD", _("Credit Card")
    PAYPAL = "PAYPAL", _("PayPal")
    BANK_TRANSFER = "BANK_TRANSFER", _("Bank Transfer")
    CASH_ON_DELIVERY = "CASH_ON_DELIVERY", _("Cash on Delivery")
    GIFT_CARD = "GIFT_CARD", _("Gift Card")
    DIRECT_DEBIT = "DIRECT_DEBIT", _("Direct Debit")
    CASH_IN_STORE = "CASH_IN_STORE", _("Cash in Store")
    MFS = "MFS", _("Mobile Financial Services")
    CARRIER_BILLING = "CARRIER_BILLING", _("Carrier Billing")
    CRYPTOCURRENCY = "CRYPTOCURRENCY", _("Cryptocurrency")
    BUY_NOW_PAY_LATER = "BUY_NOW_PAY_LATER", _("Buy Now, Pay Later")
    E_WALLET = "E_WALLET", _("E-Wallet")
    BANK_TRANSFER_INSTANT = "BANK_TRANSFER_INSTANT", _("Instant Bank Transfer")
    POSTAL_MONEY_ORDER = "POSTAL_MONEY_ORDER", _("Postal Money Order")
    CHEQUE = "CHEQUE", _("Cheque")
    OTHER = "OTHER", _("Other")
