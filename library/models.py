from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class LibraryEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="library_entries",
    )
    game = models.ForeignKey(
        "games.Game", on_delete=models.CASCADE, related_name="library_entries"
    )

    # Status choices
    STATUS_CHOICES = [
        ("playing", "Playing"),
        ("completed", "Completed"),
        ("backlog", "Backlog"),
        ("dropped", "Dropped"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="backlog")

    # Optional fields
    hours_played = models.PositiveIntegerField(null=True, blank=True)
    personal_rating = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Source(models.TextChoices):
        STEAM = "steam", "Steam"
        GOG = "gog", "GOG"
        EPIC = "epic", "Epic Games Store"
        OTHER = "other", "Other"

    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        default=Source.OTHER,
        verbose_name="Source",
    )
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "game")
        ordering = ["-created_at"]
        verbose_name = "Library Entry"
        verbose_name_plural = "Library Entries"

    def __str__(self):
        return f"{self.user.username} - {self.game.title} ({self.status})"
