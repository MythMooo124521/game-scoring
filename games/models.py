from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class Game(models.Model):

    # Identifiers
    title = models.CharField(max_length=255, verbose_name="Game Title")
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    # Metadata
    genre = models.CharField(
        max_length=50, blank=True
    )  # Consider using a separate Genre model for better normalization

    description = models.TextField(blank=True, verbose_name="Game Description")
    developer = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    age_rating = models.CharField(max_length=10, blank=True, verbose_name="Age Rating")

    languages = models.CharField(
        max_length=255, blank=True, verbose_name="Supported Languages"
    )  # Consider using a ManyToManyField to a Language model for better normalization

    release_date = models.DateField(null=True, blank=True, verbose_name="Release Date")

    cover_image_url = models.URLField(
        max_length=500, blank=True, verbose_name="Cover Image URL"
    )

    metacritic_score = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Metacritic Score",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    # Outside IDS
    steam_app_id = models.IntegerField(
        null=True, blank=True, unique=True, verbose_name="Steam App ID"
    )
    igdb_id = models.IntegerField(
        null=True, blank=True, unique=True, verbose_name="IGDB ID"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Game"
        verbose_name_plural = "Games"

    def __str__(self):
        return f"{self.title}({self.release_date.year if self.release_date else 'N/A'})"
