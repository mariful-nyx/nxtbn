import graphene

from nxtbn.product.admin_mutations import ProductMutation
from nxtbn.product.admin_queries import ProductQuery
from nxtbn.users.admin_mutation import UserMutation
from nxtbn.order.admin_queries import AdminOrderQuery




class Query(ProductQuery, AdminOrderQuery):
    pass

class Mutation(UserMutation, ProductMutation):
    pass

admin_schema = graphene.Schema(query=Query, mutation=Mutation)
