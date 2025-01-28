from nxtbn.users.utils.jwt_utils import JWTManager
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

class NXTBNGraphQLAuthenticationMiddleware:
    def __init__(self):
        self.jwt_manager = JWTManager()

    def resolve(self, next, root, info, **args):
        request = info.context

        # First check JWT token
        user = self.get_user_from_jwt(request)
        
        # If no JWT token, fall back to session-based authentication
        if not user.is_authenticated:
            user = self.get_user_from_session(request)

        # If no valid user from either method, set as AnonymousUser
        if not user.is_authenticated:
            user = AnonymousUser()

        info.context.user = user

        # Continue processing the query
        return next(root, info, **args)

    def get_user_from_jwt(self, request):
        token = self.get_token_from_request(request)
        if token:
            return self.jwt_manager.verify_jwt_token(token) or AnonymousUser()
        return AnonymousUser()

    def get_user_from_session(self, request):
        return request.user if request.user.is_authenticated else AnonymousUser()

    def get_token_from_request(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]

        return request.COOKIES.get("access_token")
