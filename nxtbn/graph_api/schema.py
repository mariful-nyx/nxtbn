import graphene

from nxtbn.graph_api.queries import ProductQuery, CartQuery


class Query(ProductQuery, CartQuery):
    pass
    

schema = graphene.Schema(query=Query)
