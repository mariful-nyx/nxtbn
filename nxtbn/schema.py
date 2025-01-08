import graphene

from nxtbn.cart.mutation import CartMutation
from nxtbn.order.mutation import OrderMutation
from nxtbn.product.queries import ProductQuery
from nxtbn.cart.queries import CartQuery



class Query(ProductQuery, CartQuery):
    pass

class Mutation(CartMutation, OrderMutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
