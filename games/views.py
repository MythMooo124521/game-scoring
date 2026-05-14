# Create your views here.
from django.shortcuts import get_object_or_404, render

from games.models import Game


def game_list(request):
    games = Game.objects.all()
    return render(request, "games/game_list.html", {"games": games})


def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    return render(request, "games/game_detail.html", {"game": game})
