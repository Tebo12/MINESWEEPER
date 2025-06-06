from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import RegisterForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm
    form = RegisterForm
    model = CustomUser
    list_display = ['email', 'username', ]


admin.site.register(CustomUser, CustomUserAdmin)
