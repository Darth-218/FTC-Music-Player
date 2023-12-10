import sys
sys.path.append('./')
import api_client.Youtube.youtube as yt
import api_client.Youtube.api_models as yt_models
import flet as ft
import SearchResults

def main(page: ft.Page):
    request = yt_models.SearchRequest(query="Jacob's Piano", artist_count=1, album_count=3, song_count=20)
    results = yt.search(request=request)
    searchResultsWidget = SearchResults.SearchResults(results=results)
    page.add(searchResultsWidget)

ft.app(main)