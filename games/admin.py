from django.contrib import admin

from games.models import Game

# Register your models here.


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "developer",
        "genre",
        "release_date",
        "metacritic_score",
        "steam_app_id",
        "igdb_id",
    )
    list_filter = ("genre", "release_date")
    search_fields = ("title", "developer", "description")
    ordering = ("-release_date",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
