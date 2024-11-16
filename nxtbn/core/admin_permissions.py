from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from nxtbn.users import UserRole

class NxtbnAdminPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True

        return False


class RoleBasedPermission(BasePermission):
    """
    Generic permission class that checks role-based permissions
    defined at the view level in ROLE_PERMISSIONS.
    """
    def has_permission(self, request, view):
        user = request.user

        # Ensure the user is authenticated
        if not user.is_authenticated:
            return False

        # Retrieve role-based permissions from the view
        role_permissions = getattr(view, 'ROLE_PERMISSIONS', {})

        # Get the user's role
        user_role = getattr(user, 'role', None)

        # Determine allowed permissions for the role
        allowed_permissions = role_permissions.get(user_role, set())

        # Check for full access or read-only access
        if "all" in allowed_permissions:
            return True
        if "read-only" in allowed_permissions and request.method in SAFE_METHODS:
            return True

        # Deny access otherwise
        return False