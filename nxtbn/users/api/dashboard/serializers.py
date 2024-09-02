from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db import transaction

from nxtbn.users.admin import User


class DashboardLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'avatar', 'username', 'email', 'first_name', 'last_name', 'role']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'avatar', 'username', 'email', 'first_name', 'last_name', 'full_name', 'role']