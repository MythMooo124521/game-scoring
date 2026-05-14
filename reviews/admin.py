from django.contrib import admin

from reviews.models import Review


# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "game",
        "rating",
        "is_recommended",
        "created_at",
    )
    list_filter = ("rating", "is_recommended", "created_at")
    search_fields = ("user__username", "game__title", "review_text")
    ordering = ("-created_at",)
