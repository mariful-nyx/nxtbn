import graphene
from graphene_django.types import DjangoObjectType
from nxtbn.users.models import User


class AdminUserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
        interfaces = (graphene.relay.Node, )

    full_name = graphene.String()

    def resolve_full_name(self, info):
        if not self.first_name and not self.last_name:
            return self.username
        return f"{self.first_name} {self.last_name}"

