import graphene
from nxtbn.product.admin_types import ProductTranslationType
from nxtbn.product.models import ProductTranslation



class UpdateProductTranslatoinMutation(graphene.Mutation):
    class Arguments:
        base_product_id = graphene.Int(required=True)
        lang_code = graphene.String(required=True)
        name = graphene.String()
        summary = graphene.String()
        description = graphene.String()
        meta_title = graphene.String()
        meta_description = graphene.String()

    product_translation = graphene.Field(ProductTranslationType)

    def mutate(self, info, base_product_id, lang_code, name, summary, description, meta_title, meta_description):
        try:
            product_translation = ProductTranslation.objects.get(product_id=base_product_id, language_code=lang_code)
        except ProductTranslation.DoesNotExist:
            product_translation = ProductTranslation(product_id=base_product_id, language_code=lang_code)

        product_translation.name = name
        product_translation.summary = summary
        product_translation.description = description
        product_translation.meta_title = meta_title
        product_translation.meta_description = meta_description
        product_translation.save()

        return UpdateProductTranslatoinMutation(product_translation=product_translation) 



class ProductMutation(graphene.ObjectType):
    update_product_translation = UpdateProductTranslatoinMutation.Field()