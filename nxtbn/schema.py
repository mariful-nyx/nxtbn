import graphene

from nxtbn.product.mutation import CartMutation
from nxtbn.product.queries import ProductQuery, CartQuery


class Query(ProductQuery, CartQuery):
    pass

class Mutation(CartMutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
