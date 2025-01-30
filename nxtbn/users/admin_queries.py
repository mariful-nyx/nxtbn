import graphene

from nxtbn.users.admin_types import PermissionType
from django.contrib.auth.models import Permission

from nxtbn.users.models import User


class UserAdminQuery(graphene.ObjectType):
    permissions = graphene.List(PermissionType, user_id=graphene.Int(required=True))

    def resolve_permissions(self, info, user_id):
        # Get the user by the provided user_id
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return []  # If the user doesn't exist, return an empty list

        # Retrieve all permissions from the database
        permissions = Permission.objects.all()

        # Create a list of PermissionType objects with the user permission check
        permission_data = []
        for permission in permissions:
            permission_data.append(PermissionType(
                codename=permission.codename,
                name=permission.name,
                has_assigned=user.has_perm(f'{permission.codename}')  # Check if the user has the permission
            ))
        return permission_data