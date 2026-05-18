import requests
from django.conf import settings


class SteamAPI:
    """Wrapper do Steam Web API."""

    BASE_URL = "https://api.steampowered.com"
    STORE_URL = "https://store.steampowered.com/api"

    def __init__(self):
        self.api_key = settings.STEAM_API_KEY

    def get_owned_games(self, steam_id):
        """
        Pobiera listę gier z biblioteki użytkownika.
        Zwraca listę gier albo pustą listę jeśli błąd.
        """
        url = f"{self.BASE_URL}/IPlayerService/GetOwnedGames/v1/"
        params = {
            "key": self.api_key,
            "steamid": steam_id,
            "include_appinfo": 1,  # dołącz nazwę i ikonki
            "include_played_free_games": 1,  # dołącz darmowe gry
            "format": "json",
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  # rzuć błąd jeśli status != 200
            data = response.json()
            games = data.get("response", {}).get("games", [])
            return games
        except requests.exceptions.Timeout:
            print("Steam API timeout")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Steam API error: {e}")
            return []

    def get_game_details(self, app_id):
        """
        Pobiera szczegóły gry ze Steam Store API.
        Zwraca słownik z danymi albo None jeśli błąd.
        """
        url = f"{self.STORE_URL}/appdetails/"
        params = {
            "appids": app_id,
            "l": "english",
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Steam zwraca {app_id: {success: True/False, data: {...}}}
            app_data = data.get(str(app_id), {})

            if not app_data.get("success"):
                return None

            return app_data.get("data", {})

        except requests.exceptions.Timeout:
            print(f"Steam Store API timeout for app {app_id}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Steam Store API error: {e}")
            return None

    def parse_game_data(self, app_id, steam_game, store_data=None):
        """
        Mapuje dane ze Steam API na pola modelu Game.

        steam_game = dane z GetOwnedGames (name, playtime_forever, img_icon_url)
        store_data = dane ze Store API (description, developer, genre itd.)

        Zwraca słownik gotowy do Game.objects.create(**data)
        """
        from django.utils.text import slugify

        title = steam_game.get("name", f"Unknown Game {app_id}")
        slug = slugify(title)

        # Podstawowe dane zawsze dostępne z GetOwnedGames
        game_data = {
            "title": title,
            "slug": slug,
            "steam_app_id": app_id,
            "cover_image_url": f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/header.jpg",
        }

        # Szczegółowe dane ze Store API (opcjonalne)
        if store_data:
            game_data["description"] = store_data.get("short_description", "")
            game_data["developer"] = ", ".join(store_data.get("developers", []))
            game_data["publisher"] = ", ".join(store_data.get("publishers", []))

            # Gatunki - bierzemy pierwszy
            genres = store_data.get("genres", [])
            if genres:
                game_data["genre"] = genres[0].get("description", "")

            # Data wydania
            release = store_data.get("release_date", {})
            if release and not release.get("coming_soon"):
                from datetime import datetime

                date_str = release.get("date", "")
                if date_str:
                    try:
                        # Steam zwraca datę jako "18 May, 2015" albo "May 18, 2015"
                        for fmt in ["%d %b, %Y", "%b %d, %Y", "%d %B, %Y"]:
                            try:
                                game_data["release_date"] = datetime.strptime(
                                    date_str, fmt
                                ).date()
                                break
                            except ValueError:
                                continue
                    except Exception:
                        pass

            # Metacritic
            metacritic = store_data.get("metacritic", {})
            if metacritic:
                game_data["metacritic_score"] = metacritic.get("score")

            # Języki
            game_data["languages"] = store_data.get("supported_languages", "")

        return game_data
