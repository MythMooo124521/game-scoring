# Create your views here.
from django.shortcuts import get_object_or_404, render

from games.models import Game


def game_list(request):
    games = Game.objects.all()
    return render(request, "games/game_list.html", {"games": games})


def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)

    # Jeśli gra nie ma opisu i ma steam_app_id - pobierz szczegóły
    if game.steam_app_id and not game.description:
        from integrations.steam import SteamAPI

        steam = SteamAPI()
        store_data = steam.get_game_details(game.steam_app_id)
        if store_data:
            game.description = store_data.get("short_description", "")
            game.developer = ", ".join(store_data.get("developers", []))
            game.publisher = ", ".join(store_data.get("publishers", []))
            genres = store_data.get("genres", [])
            if genres:
                game.genre = genres[0].get("description", "")
            metacritic = store_data.get("metacritic", {})
            if metacritic:
                game.metacritic_score = metacritic.get("score")
            game.save()

    return render(request, "games/game_detail.html", {"game": game})
