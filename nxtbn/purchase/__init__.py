from django.db import models

class PurchaseStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    PENDING = 'PENDING', 'Pending'
    RECEIVED = 'RECEIVED', 'Received'
    CANCELLED = 'CANCELLED', 'Cancelled'