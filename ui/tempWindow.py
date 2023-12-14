import sys
sys.path.append('./')
import api_client.Youtube.youtube as yt
import api_client.Youtube.api_models as yt_models
import flet as ft
import SearchResults

def main(page: ft.Page):
    # request = yt_models.SearchRequest(query="Jacob's Piano", artist_count=3, album_count=3, song_count=10)
    # results = yt.search(request=request)

    request = yt_models.GetSuggestionsRequest(artist_count=3, album_count=3, song_count=5)
    results1 = yt.getSuggestions(request=request)
    results = yt_models.SearchResponse(artists=results1.artists, albums=results1.albums, songs=results1.songs, has_error=False, error="")
    print('finished getting suggestions')

    searchResultsWidget = SearchResults.SearchResults(results=results)
    page.add(searchResultsWidget)

ft.app(main)