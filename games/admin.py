from django.contrib import admin

from games.models import Game

# Register your models here.

admin.site.register(
    Game
)  # Better to use a ModelAdmin for more control over the admin interface, but this is fine for now.
