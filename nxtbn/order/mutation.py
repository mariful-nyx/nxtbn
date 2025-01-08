

import graphene

from nxtbn.order.proccesor.mutation import OrderProcessMutation


class OrderMutation(graphene.ObjectType):
    order_process = OrderProcessMutation.Field()


