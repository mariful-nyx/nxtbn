from rest_framework.permissions import BasePermission

class NxtbnAdminPermission(BasePermission):
    """
    Generic permission class that dynamically checks permissions for any model and action.
    """

    def has_permission(self, request, view):
        user = request.user

        # Ensure the user is authenticated
        if not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True

        # Dynamically get the model name from the view's queryset or model attribute
        model = getattr(view, 'queryset', None) or getattr(view, 'model', None)

        if model is None:
            return False  # No model, no permissions

        # Generate the permission codename based on the action (e.g., 'can_add', 'can_change', 'can_delete', etc.)
        action = view.action  # This is the DRF view's action (e.g., 'create', 'list', 'update', etc.)

        if action == 'create':
            perm_codename = f'{model._meta.app_label}.add_{model._meta.model_name}'
        elif action in ['update', 'partial_update']:
            perm_codename = f'{model._meta.app_label}.change_{model._meta.model_name}'
        elif action == 'destroy':
            perm_codename = f'{model._meta.app_label}.delete_{model._meta.model_name}'
        elif action == 'list' or action == 'retrieve':
            perm_codename = f'{model._meta.app_label}.view_{model._meta.model_name}'
        else:
            # Handle custom actions (e.g., 'cancel', 'ship', etc.)
            perm_codename = f'{model._meta.app_label}.{action}_{model._meta.model_name}'

        # Check if the user has the generated permission
        return user.has_perm(perm_codename)