import graphene

from nxtbn.cart.admin_query import AdminCartQuery
from nxtbn.core.admin_mutation import CoreMutation
from nxtbn.core.admin_queries import AdminCoreQuery
from nxtbn.product.admin_mutations import ProductMutation
from nxtbn.product.admin_queries import ProductQuery
from nxtbn.users.admin_mutation import AdminUserMutation
from nxtbn.order.admin_queries import AdminOrderQuery
from nxtbn.users.admin_queries import UserAdminQuery
from nxtbn.warehouse.admin_queries import WarehouseQuery





class Query(ProductQuery, AdminOrderQuery, AdminCoreQuery, WarehouseQuery, AdminCartQuery, UserAdminQuery):
    pass

class Mutation(AdminUserMutation, ProductMutation, CoreMutation):
    pass

admin_schema = graphene.Schema(query=Query, mutation=Mutation)
