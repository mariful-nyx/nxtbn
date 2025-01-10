from nxtbn.users.utils.jwt_utils import JWTManager
from django.contrib.auth.models import AnonymousUser

class GraphQLJWTMiddleware:
    def __init__(self):
        self.jwt_manager = JWTManager()

    def resolve(self, next, root, info, **args):
        request = info.context

        token = self.get_token_from_request(request)

        if token:
            user = self.jwt_manager.verify_jwt_token(token)
            if user:
                info.context.user = user
            else:
                info.context.user = AnonymousUser()
        else:
            info.context.user = AnonymousUser()

        # Continue processing the query
        return next(root, info, **args)

    def get_token_from_request(self, request):
        """Extract the token from the Authorization header or cookies."""
        # Check Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]

        # Fallback to cookies
        return request.COOKIES.get("access_token")
