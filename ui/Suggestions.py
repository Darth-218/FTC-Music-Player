import flet as ft
import api_client.Youtube.api_models as yt_models
import ArtistWidget
import AlbumWidget
import SongWidget
import HorizontalListView

class SuggestionsWidget(ft.ListView):
    suggestions: yt_models.GetSuggestionsResponse
    def __init__(self, results: yt_models.GetSuggestionsResponse):
        self.suggestions = results
        super().__init__(expand=1)

        artists = HorizontalListView.HorizontalListView()
        albums = HorizontalListView.HorizontalListView()
        songs = HorizontalListView.HorizontalListView()
        
        if len(self.suggestions.songs) > 0:
            self.controls.append(ft.Container(content=ft.Text('Try listening to', font_family='lilitaone', size=40), padding=ft.Padding(top=20, bottom=10, left=55, right=0)))
            for song in self.suggestions.songs:
                songs.append(SongWidget.SquareSongWidget(song=song))
        self.controls.append(ft.Container(content=songs, bgcolor='#ffffff5', padding=ft.Padding(top=20, bottom=20, left=20, right=20), border_radius=25))

        if len(self.suggestions.albums) > 0:
            self.controls.append(ft.Container(content=ft.Text('Made for you', font_family='lilitaone', size=40), padding=ft.Padding(top=20, bottom=10, left=55, right=0)))
            for album in self.suggestions.albums:
                albums.append(AlbumWidget.SquareAlbumWidget(album=album))
        self.controls.append(ft.Container(content=albums, bgcolor='#ffffff5', padding=ft.Padding(top=20, bottom=20, left=20, right=20), border_radius=25))

        if len(self.suggestions.artists) > 0:
            self.controls.append(ft.Container(content=ft.Text('Artists you might like', font_family='lilitaone', size=40), padding=ft.Padding(top=20, bottom=10, left=55, right=0)))
            for artist in self.suggestions.artists:
                artists.append(ArtistWidget.SquareArtistWidget(artist=artist))
        self.controls.append(ft.Container(content=artists, bgcolor='#ffffff5', padding=ft.Padding(top=20, bottom=20, left=20, right=20), border_radius=25))
