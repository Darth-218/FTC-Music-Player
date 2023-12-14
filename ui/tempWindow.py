import sys
sys.path.append('./')
import api_client.Youtube.youtube as yt
import api_client.Youtube.api_models as yt_models
import flet as ft
import SearchResults
import Suggestions
from queue import Queue

def main(page: ft.Page):
    page.fonts = {
        "lilitaone": "./Assets/Fonts/LilitaOne-Regular.ttf"
    }
    # request = yt_models.SearchRequest(query="Jacob's Piano", artist_count=3, album_count=3, song_count=10)
    # results = yt.search(request=request)

    # searchResultsWidget = SearchResults.SearchResults(results=results)
    # page.add(searchResultsWidget)

    page.add(ft.Container(content=ft.ProgressRing(), alignment=ft.alignment.center, expand=True))
    request = yt_models.GetSuggestionsRequest(artist_count=3, album_count=3, song_count=5)
    results = yt.getSuggestions(request=request)
    page.remove(page.controls[0])
    suggestions = Suggestions.SuggestionsWidget(results=results)
    page.add(suggestions)

    page.update()

ft.app(main)