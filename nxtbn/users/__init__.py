from django.db import models

class UserRole(models.TextChoices):
    """Defines user roles for the application.

    - 'ADMIN': Represents an administrative user with full permissions.
    - 'CUSTOMER': Represents a customer or end-user.
    - 'STAFF': Represents a staff member with limited permissions.
    """

    ADMIN = 'ADMIN', 'Admin'
    CUSTOMER = 'CUSTOMER', 'Customer'
    STAFF = 'STAFF', 'Staff'
