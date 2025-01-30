import graphene

from nxtbn.users.admin_types import PermissionType
from django.contrib.auth.models import Permission

from nxtbn.users.models import User


class UserAdminQuery(graphene.ObjectType):
    permissions = graphene.List(PermissionType, user_id=graphene.Int(required=True))

    def resolve_permissions(self, info, user_id):
        # Get the user by the provided user_id
        try:
            user = User.objects.prefetch_related('user_permissions').get(id=user_id)
        except User.DoesNotExist:
            return []  # If the user doesn't exist, return an empty list

        # Retrieve all permissions from the database
        permissions = Permission.objects.all()

        # Create a set of user's permissions for quick lookup
        user_permissions = set(user.user_permissions.all())

        # Create a list of PermissionType objects with the user permission check
        permission_data = [
            PermissionType(
                codename=permission.codename,
                name=permission.name,
                has_assigned=permission in user_permissions  # Check if the user has the permission
            )
            for permission in permissions
        ]
        return permission_data