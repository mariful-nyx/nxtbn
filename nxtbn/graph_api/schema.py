import graphene

from nxtbn.graph_api.mutation import CartMutation
from nxtbn.graph_api.queries import ProductQuery, CartQuery


class Query(ProductQuery, CartQuery):
    pass

class Mutation(CartMutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
