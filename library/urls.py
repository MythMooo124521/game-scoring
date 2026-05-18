from django.urls import path

from library import views

urlpatterns = [
    path("library/", views.library_view, name="library"),
    path(
        "library/import/steam/", views.import_steam_library, name="import_steam_library"
    ),
    path("library/add/<slug:slug>/", views.add_to_library, name="add_to_library"),
    path(
        "library/remove/<slug:slug>/",
        views.remove_from_library,
        name="remove_from_library",
    ),
]
