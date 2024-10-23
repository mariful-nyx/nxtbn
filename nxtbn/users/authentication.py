from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from nxtbn.users.utils.jwt_utils import JWTManager

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        jwt_manager = JWTManager()
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            user = jwt_manager.verify_jwt_token(token)
            if user:
                return (user, None)
            raise AuthenticationFailed({"detail": "Invalid or expired token", "code": "token_invalid_or_expired"})
        return None
