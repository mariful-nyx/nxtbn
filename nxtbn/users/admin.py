
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (("User", {"fields": ('avatar', "role",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "first_name", "email", "is_superuser", "is_active", "is_staff", "role"]
    search_fields = ["first_name", "email",]

