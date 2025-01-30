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


class GranularPermission(BasePermission):
    def get_permission_name(self, model_name, action):
       
        return f"{model_name}.{action}"

    def has_permission(self, request, view):
      
        model_name = view.queryset.model.__name__.lower()  # Get model name dynamically
        action = view.action.required_perm

        permission_name = self.get_permission_name(model_name, action)

        # Check if the user has the generated permission
        return request.user.has_perm(permission_name)


def check_user_permissions(info, any_staff=False, allowed_roles=[]):
    if not info.context.user.is_authenticated:
        raise Exception("You must be logged in to perform this action")
    
    if not info.context.user.is_staff:
        raise Exception("You must be a staff to perform this action")
    
    if info.context.user.is_superuser:
        return True
    
    if any_staff:
        return True
    
    if info.context.user.role not in allowed_roles:
        raise Exception("You do not have permission to perform this action")
    
    return True