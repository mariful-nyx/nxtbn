from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from nxtbn.users import UserRole


import functools
from graphql import GraphQLError

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

class GranularPermission(BasePermission):
    def get_permission_name(self, model_name, action):
       
        return f"{model_name}.{action}"

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if request.method in SAFE_METHODS and request.user.is_staff: # Every staff can view
            return True
      
        model_cls = getattr(view, 'queryset', None) or getattr(view, 'model', None)
        if model_cls is None:
            return False

        model_name = model_cls.__name__.lower()
        action = view.required_perm

        permission_name = self.get_permission_name(model_name, action)

        # Check if the user has the generated permission
        return request.user.has_perm(permission_name)
    

class CommonPermissions(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if request.method in SAFE_METHODS and request.user.is_staff: # Every staff can view
            return True



        model_cls = getattr(view, 'queryset', None) or getattr(view, 'model', None)
        if model_cls is None:
            return False

        model_meta = model_cls.model._meta

        method_permissions_map = {
            'GET': f'{model_meta.app_label}.view_{model_meta.model_name}',
            'OPTIONS': f'{model_meta.app_label}.view_{model_meta.model_name}',
            'HEAD': f'{model_meta.app_label}.view_{model_meta.model_name}',
            'POST': f'{model_meta.app_label}.add_{model_meta.model_name}',
            'PUT': f'{model_meta.app_label}.change_{model_meta.model_name}',
            'PATCH': f'{model_meta.app_label}.change_{model_meta.model_name}',
            'DELETE': f'{model_meta.app_label}.delete_{model_meta.model_name}',
        }

        required_permission = method_permissions_map.get(request.method)

        if required_permission is None:
            return False

        return request.user.has_perm(required_permission)


def has_required_perm(user, code: str, model_cls=None):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    perm_code  = model_cls._meta.app_label + '.' + code
    return user.has_perm(perm_code)


def gql_required_perm(code: str): # Used in graphql only
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, info, *args, **kwargs):
            operation = info.operation.operation
            user = info.context.user

            if user.is_anonymous:
                raise GraphQLError("Authentication required")

            if operation == "query":
                return func(self, info, *args, **kwargs)

            
            
            if not user.has_perm(code):  # Check if user has the required permission
                raise GraphQLError("Permission denied")  # Block unauthorized access

            return func(self, info, *args, **kwargs)  # Call the actual resolver
        
        return wrapper
    
    return decorator



def gql_staff_required(func): # Used in graphql only
    @functools.wraps(func)
    def wrapper(self, info, *args, **kwargs):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Authentication required")

        if not user.is_staff:  # Check if the user is a staff member
            raise GraphQLError("Permission denied")  # Block access if the user is not staff

        return func(self, info, *args, **kwargs)  # Call the actual resolver

    return wrapper