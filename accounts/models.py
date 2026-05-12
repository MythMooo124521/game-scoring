from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    # User Profile
    bio = models.TextField(blank=True, verbose_name="User Bio")
    avatar_url = models.URLField(
        max_length=500, blank=True, verbose_name="Avatar Image URL"
    )

    # IDs
    steam_id = models.CharField(
        max_length=255, blank=True, unique=True, null=True, verbose_name="Steam ID"
    )  # TODO: Consider using a separate SteamProfile model for better separation of concerns
    is_public = models.BooleanField(default=True, verbose_name="Public Profile")
    steam_username = models.CharField(
        max_length=255, blank=True, verbose_name="Steam Username"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.username}'s Profile"
