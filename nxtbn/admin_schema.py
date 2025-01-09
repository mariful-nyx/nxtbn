import graphene

from nxtbn.product.admin_mutations import ProductMutation
from nxtbn.product.admin_queries import ProductTranslationQuery
from nxtbn.users.admin_mutation import UserMutation




class Query(ProductTranslationQuery):
    pass

class Mutation(UserMutation, ProductMutation):
    pass

admin_schema = graphene.Schema(query=Query, mutation=Mutation)
