from django.urls import path

from nxtbn.users.api.storefront.views import LoginView, SignupView, LogoutView, TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='customer_signup'),
    path('login/', LoginView.as_view(), name='customer_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
