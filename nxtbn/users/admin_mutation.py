import graphene
from django.contrib.auth import authenticate

from django.conf import settings

from nxtbn.users.api.storefront.serializers import JwtBasicUserSerializer
from nxtbn.users.utils.jwt_utils import JWTManager

class AdminTokenType(graphene.ObjectType):
    access = graphene.String()
    refresh = graphene.String()
    expiresIn = graphene.Int()
    refreshExpiresIn = graphene.Int()

class AdminLoginUserType(graphene.ObjectType):
    id = graphene.ID()
    email = graphene.String()
    username = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()
    full_name = graphene.String()
    role = graphene.String()

class AdminLoginResponse(graphene.ObjectType):
    user = graphene.Field(AdminLoginUserType)
    storeUrl = graphene.String()
    version = graphene.String()
    base_currency = graphene.String()
    token = graphene.Field(AdminTokenType)

class AdminLoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    login = graphene.Field(AdminLoginResponse)

    def mutate(self, info, email, password):
        jwt_manager = JWTManager()

        user = authenticate(email=email, password=password)
        if user:
            if not user.is_staff:
                raise Exception("Only staff members can log in.")
            
            if not user.is_active:
                raise Exception("User is not active.")

            access_token = jwt_manager.generate_access_token(user)
            refresh_token = jwt_manager.generate_refresh_token(user)

            user_data = JwtBasicUserSerializer(user).data

            response = AdminLoginResponse(
                user=AdminLoginUserType(**user_data),
                storeUrl=settings.STORE_URL,
                version=settings.VERSION,
                base_currency=settings.BASE_CURRENCY,
                token=AdminTokenType(
                    access=access_token,
                    refresh=refresh_token,
                    expiresIn=jwt_manager.access_token_expiration_seconds,
                    refreshExpiresIn=jwt_manager.refresh_token_expiration_seconds
                )
            )

            return AdminLoginMutation(login=response)
        else:
            raise Exception("Invalid credentials")
        



class AdminTokenRefreshMutation(graphene.Mutation):
    class Arguments:
        refresh_token = graphene.String(required=True)

    refresh = graphene.Field(AdminLoginResponse)

    def mutate(self, info, refresh_token):
        jwt_manager = JWTManager()

        # Verify refresh token
        user = jwt_manager.verify_jwt_token(refresh_token)

        if user:
            access_token = jwt_manager.generate_access_token(user)
            new_refresh_token = jwt_manager.generate_refresh_token(user)

            user_data = JwtBasicUserSerializer(user).data

            response = AdminLoginResponse(
                user=AdminLoginUserType(**user_data),
                storeUrl=settings.STORE_URL,
                version=settings.VERSION,
                base_currency=settings.BASE_CURRENCY,
                token=AdminTokenType(
                    access=access_token,
                    refresh=new_refresh_token,
                    expiresIn=jwt_manager.access_token_expiration_seconds,
                    refreshExpiresIn=jwt_manager.refresh_token_expiration_seconds
                )
            )

            return AdminTokenRefreshMutation(refresh=response)
        else:
            raise Exception("Invalid or expired refresh token")

class AdminUserMutation(graphene.ObjectType):
    login = AdminLoginMutation.Field()
    refresh_token = AdminTokenRefreshMutation.Field()
