from django.shortcuts import get_object_or_404, redirect, render

from games.models import Game
from reviews.forms import ReviewForm


# Create your views here.
def add_review(request, slug):
    game = get_object_or_404(Game, slug=slug)

    if not request.user.is_authenticated:
        return redirect("account_login")

    if request.method == "POST":
        # Stwórz formularz z danymi z POST
        form = ReviewForm(request.POST)

        if form.is_valid():
            # KROK 4: Zapisz recenzję
            review = form.save(commit=False)
            review.user = request.user
            review.game = game
            review.save()

            # KROK 5: Przekieruj na stronę gry
            return redirect("game_detail", slug=game.slug)
    else:
        # GET request - pusty formularz
        form = ReviewForm()

    # KROK 6: Pokaż stronę z formularzem
    return render(
        request,
        "reviews/add_review.html",
        {
            "form": form,
            "game": game,
        },
    )
