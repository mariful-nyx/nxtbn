import graphene
from django.contrib.auth import authenticate

from django.conf import settings

from nxtbn.users.api.storefront.serializers import JwtBasicUserSerializer
from nxtbn.users.utils.jwt_utils import JWTManager

class TokenType(graphene.ObjectType):
    access = graphene.String()
    refresh = graphene.String()
    expiresIn = graphene.Int()
    refreshExpiresIn = graphene.Int()

class UserType(graphene.ObjectType):
    id = graphene.ID()
    email = graphene.String()
    username = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()
    full_name = graphene.String()
    role = graphene.String()

class LoginResponse(graphene.ObjectType):
    user = graphene.Field(UserType)
    storeUrl = graphene.String()
    version = graphene.String()
    token = graphene.Field(TokenType)

class LoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    login = graphene.Field(LoginResponse)

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

            response = LoginResponse(
                user=UserType(**user_data),
                storeUrl=settings.STORE_URL,
                version=settings.VERSION,
                token=TokenType(
                    access=access_token,
                    refresh=refresh_token,
                    expiresIn=jwt_manager.access_token_expiration_seconds,
                    refreshExpiresIn=jwt_manager.refresh_token_expiration_seconds
                )
            )

            return LoginMutation(login=response)
        else:
            raise Exception("Invalid credentials")

class UserMutation(graphene.ObjectType):
    login = LoginMutation.Field()
