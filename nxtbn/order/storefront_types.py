from graphene_django import DjangoObjectType
from nxtbn.order.models import Address

class AddressGraphType(DjangoObjectType):
    class Meta:
        model = Address
        fields = (
            'id',
            'first_name',
            'last_name',
            'company_name',
            'street_address',
            'city',
            'postal_code',
            'country',
            'phone',
            'email',
            'address_type',
            'created_at',
            'updated_at',
        )
