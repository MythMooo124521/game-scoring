from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    # Columns shown in admin list view
    list_display = (
        "id",
        "username",
        "email",
        "steam_id",
        "steam_username",
        "is_public",
        "is_staff",
        "date_joined",
    )

    # Filters in sidebar
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "is_public",
    )

    # Search fields
    search_fields = (
        "username",
        "email",
        "steam_id",
        "steam_username",
    )

    ordering = ("-date_joined",)

    # Fields shown in user edit page
    fieldsets = UserAdmin.fieldsets + (
        (
            "Profile Information",
            {
                "fields": (
                    "bio",
                    "avatar_url",
                    "steam_id",
                    "steam_username",
                    "is_public",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    # Make timestamps readonly
    readonly_fields = (
        "created_at",
        "updated_at",
        "date_joined",
        "last_login",
    )
