from django.contrib import admin

from library.models import LibraryEntry


# Register your models here.
@admin.register(LibraryEntry)
class LibraryEntryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "game",
        "created_at",
        "hours_played",
        "status",
        "source",
        "personal_rating",
    )
    list_filter = ("status", "source", "created_at")
    search_fields = ("user__username", "game__title")
    ordering = ("-created_at",)
