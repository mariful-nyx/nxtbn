

import graphene

from nxtbn.order.proccesor.storefront_mutation import OrderProcessMutation


class OrderMutation(graphene.ObjectType):
    order_process = OrderProcessMutation.Field()


