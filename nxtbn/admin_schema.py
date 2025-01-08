import graphene

from nxtbn.product.storefront_queries import ProductQuery
from nxtbn.users.admin_mutation import UserMutation



class Query(ProductQuery):
    pass

class Mutation(UserMutation):
    pass

admin_schema = graphene.Schema(query=Query, mutation=Mutation)
