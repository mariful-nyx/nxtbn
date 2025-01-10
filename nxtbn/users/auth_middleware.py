from nxtbn.users.utils.jwt_utils import JWTManager

class GraphQLJWTMiddleware:
    def __init__(self):
        self.jwt_manager = JWTManager()

    def resolve(self, next, root, info, **args):
        # Get the request object from info.context
        request = info.context
        # Get token from headers or cookies
        token = self.get_token_from_request(request)

        if token:
            # Verify token
            user = self.jwt_manager.verify_jwt_token(token)
            if user:
                # Attach the user to the context for access within GraphQL resolvers
                info.context.user = user
            else:
                info.context.user = None
        else:
            info.context.user = None

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
