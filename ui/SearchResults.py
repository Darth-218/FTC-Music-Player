import sys
sys.path.append('./')
import api_client.Youtube.youtube as yt
import api_client.Youtube.api_models as yt_models
import threading
import time
import ArtistWidget
import AlbumWidget
import SongWidget
import flet as ft

class SearchResults(ft.ListView):
    def __init__(self, results: yt_models.SearchResponse):
        super().__init__(expand=1, divider_thickness=2, spacing=10)
        [super().controls.append(ArtistWidget.ArtistWidget(artist=artist)) for artist in results.artists]
        [super().controls.append(AlbumWidget.AlbumWidget(album=album)) for album in results.albums]
        [super().controls.append(SongWidget.SongWidget(song=song)) for song in results.songs]

