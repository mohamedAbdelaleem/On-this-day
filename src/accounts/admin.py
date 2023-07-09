from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from . import forms
from .models import CustomUser, Profile
# Register your models here.


class CustomUserAdmin(UserAdmin):

    add_form = forms.RegisterForm
    form = forms.CustomUserChangeForm

    fieldsets = (
            (None, {"fields": ("username", "password")}),
            (("Personal info"), {"fields": ("email",)}),
            (
                ("Permissions"),
                {
                    "fields": (
                        "is_active",
                        "is_staff",
                        "is_superuser",
                        "groups",
                        "user_permissions",
                    ),
                },
            ),
            (("Important dates"), {"fields": ("last_login", "date_joined")}),
        )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )

    readonly_fields = [
        'date_joined',
    ]

    list_display = ['username', 'email',]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)


