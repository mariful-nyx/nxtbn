import graphene

from nxtbn.cart.storefront_mutation import CartMutation
from nxtbn.order.storefront_mutation import OrderMutation
from nxtbn.product.storefront_queries import ProductQuery
from nxtbn.cart.storefront_queries import CartQuery



class Query(ProductQuery, CartQuery):
    pass

class Mutation(CartMutation, OrderMutation):
    pass

admin_schema = graphene.Schema(query=Query, mutation=Mutation)
