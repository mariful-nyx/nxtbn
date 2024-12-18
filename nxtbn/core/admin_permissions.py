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
    Custom permission that grants or denies access based on the role and action.
    """
    def has_permission(self, request, view):
        user = request.user

        # Ensure user is authenticated
        if not user.is_authenticated:
            return False
        
        if user.role == UserRole.ADMIN:
            return True

        # Get the action from URL
        action = view.kwargs.get('action') or view.action



        # Check if action exists in the permissions for the user's role
        role_permissions = view.ROLE_PERMISSIONS.get(user.role, set())

        if "all" in role_permissions:
            return True

        # Grant permission if the action is allowed for the user's role
        if action in role_permissions:
            return True

        return False