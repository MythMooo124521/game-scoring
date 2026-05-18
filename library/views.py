from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.text import slugify

from games.models import Game
from integrations.steam import SteamAPI
from library.models import LibraryEntry


def import_steam_library(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to import your Steam library.")
        return redirect("account_login")

    steam_api = SteamAPI()
    steam_id = request.user.steam_id

    if not steam_id:
        messages.error(request, "Please provide a valid Steam ID.")
        return redirect("/")

    try:
        owned_games = steam_api.get_owned_games(steam_id)
    except Exception as e:
        messages.error(request, f"Error fetching Steam library: {str(e)}")
        return redirect("/")

    for game_data in owned_games:
        appid = game_data["appid"]

        # Pobierz lub stwórz grę w bazie
        if not Game.objects.filter(steam_app_id=appid).exists():
            parsed = steam_api.parse_game_data(appid, game_data, None)

            # Upewnij się że slug jest unikalny
            base_slug = slugify(parsed["title"])
            slug = base_slug
            counter = 1
            while Game.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            parsed["slug"] = slug

            game = Game.objects.create(**parsed)
        else:
            game = Game.objects.get(steam_app_id=appid)

        # Stwórz/zaktualizuj LibraryEntry
        LibraryEntry.objects.update_or_create(
            user=request.user,
            game=game,
            defaults={
                "hours_played": game_data.get("playtime_forever", 0) // 60,
                "source": LibraryEntry.Source.STEAM,
            },
        )

    messages.success(request, "Your Steam library has been imported successfully!")
    return redirect("/")


def library_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view your library.")
        return redirect("account_login")

    entries = LibraryEntry.objects.filter(user=request.user).select_related("game")
    return render(request, "library/library.html", {"entries": entries})


def add_to_library(request, slug):
    pass


def remove_from_library(request, slug):
    pass
