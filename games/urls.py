from django.urls import path

from games import views

urlpatterns = [
    path("", views.game_list, name="game_list"),
    path("games/<slug:slug>/", views.game_detail, name="game_detail"),
]
