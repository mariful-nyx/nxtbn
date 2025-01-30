import graphene
from graphene_django.types import DjangoObjectType
from nxtbn.users.models import User


class AdminUserType(DjangoObjectType):
    full_name = graphene.String()
    db_id = graphene.ID(source='id')
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
        interfaces = (graphene.relay.Node, )


    def resolve_full_name(self, info):
        if not self.first_name and not self.last_name:
            return self.username
        return f"{self.first_name} {self.last_name}"




class PermissionType(graphene.ObjectType):
    codename = graphene.String()
    name = graphene.String()
    has_assigned = graphene.Boolean()