from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "business",
        "email",
        "phone",
        "is_owner",
        "is_staff",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Business",
            {
                "fields": (
                    "business",
                    "phone",
                    "profile_image",
                    "is_owner",
                )
            },
        ),
    )