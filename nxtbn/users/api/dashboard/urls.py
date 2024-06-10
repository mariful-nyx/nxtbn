from django.urls import path
from nxtbn.users.api.dashboard import views as users_views

urlpatterns = [
    path('login/', users_views.LoginView.as_view(), name='login'),
]
