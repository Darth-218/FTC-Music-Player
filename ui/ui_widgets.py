import flet as ft
import api_client.Youtube.api_models as yt_models
import api_client.Youtube.youtube as yt
import data_models as dm
import models
import lib

class Home(ft.Container):
    def __init__(self, player: models.Player):
        self.player = player
        super().__init__()
        self.expand = True
        self.tabContent = ft.Container(content=ft.Text('Index did not change!'), expand=True)
        self.tabViewContents = [
            ft.Container(
                width=250,
                content=ft.NavigationRail(
                    width=250, 
                    selected_index = 0,
                    destinations=[
                        ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.HOME_OUTLINED, size=35), 
                                                    selected_icon_content=ft.Icon(ft.icons.HOME_ROUNDED, size=35),
                                                    label="Home"),
                        ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.SEARCH_OUTLINED, size=35), 
                                                    selected_icon_content=ft.Icon(ft.icons.SEARCH, size=35),
                                                    label="Search"),
                        ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.FIND_IN_PAGE_OUTLINED, size=35),
                                                    selected_icon_content=ft.Icon(ft.icons.FIND_IN_PAGE_ROUNDED, size=35),
                                                    label="Browse",),
                        ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.SETTINGS_OUTLINED, size=35),
                                                    selected_icon_content=ft.Icon(ft.icons.SETTINGS, size=35),
                                                    label="Settings",)
                    ],
                    on_change=lambda e: self.onContentChange(e.control.selected_index)
                ),
            ),
            self.tabContent,
        ]
        
        self.tabView = ft.Row(controls=self.tabViewContents, expand=True)
        self.content = self.tabView

    def onContentChange(self, selectedItem: int):
        match selectedItem:
            case 0:
                self.tabView.controls[1] = ft.Container(content=ft.ProgressRing(), alignment=ft.alignment.center, expand=True)
                self.update()
                request = yt_models.GetSuggestionsRequest(3, 3, 5)
                suggestions = yt.getSuggestions(request=request)
                results_widget = ft.Column(controls=[SuggestionsWidget(suggestions, player=self.player)], expand=True)
                self.tabView.controls[1] = results_widget
            case 1:
                self.tabView.controls[1] = ft.Column(controls=[Search_bar_widget()], expand=True)         
            case 2:
                self.tabView.controls[1] = ft.Text('Browse')
            case 3:
                self.tabView.controls[1] = ft.Text('Settings')
        self.update()

class ArtistWidget(ft.TextButton):
    def __init__(self, artist: yt_models.OnlineArtist):
        super().__init__(content=ft.Container(content=ft.Row(
                    [
                        ft.Image(src=artist.cover_art, width=100, height=100, border_radius=15, fit=ft.ImageFit.COVER),
                        ft.Text(artist.name)
                    ],
                ),
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
            ),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25),),
        )

class SquareArtistWidget(ft.TextButton):
    def __init__(self, artist: yt_models.OnlineArtist):
        super().__init__(content=ft.Container(content=ft.Column(
                    [
                        ft.Image(src=artist.cover_art, width=150, height=150, border_radius=75, fit=ft.ImageFit.COVER),
                        ft.Text(artist.name, text_align=ft.TextAlign.CENTER, no_wrap=True, overflow=ft.TextOverflow.FADE)
                    ],
                    alignment=ft.alignment.center,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
                alignment=ft.alignment.center,
            ),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25),),
            width=170,
        )
        

class AlbumWidget(ft.TextButton):
    def __init__(self, album: yt_models.OnlineAlbum):
        super().__init__(content=ft.Container(content=ft.Row(
                    [
                        ft.Image(src=album.cover_art, width=100, height=100, border_radius=15, fit=ft.ImageFit.COVER),
                        ft.Text(album.name)
                    ],
                ),
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
            ),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25),),
        )

class SquareAlbumWidget(ft.TextButton):
    def __init__(self, album: yt_models.OnlineAlbum):
        super().__init__(content=ft.Container(content=ft.Column(
                    [
                        ft.Image(src=album.cover_art, width=150, height=150, border_radius=15, fit=ft.ImageFit.COVER),
                        ft.Text(album.name, text_align=ft.TextAlign.CENTER, no_wrap=True, overflow=ft.TextOverflow.FADE)
                    ],
                    alignment=ft.alignment.center,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
                alignment=ft.alignment.center,
            ),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25),),
            width=170,
        )

class SongWidget(ft.TextButton):
    def __init__(self, song: dm.Song, songList: list[dm.Song], player: models.Player):
        self.songList: list[dm.Song] = songList
        self.song: yt_models.OnlineSong = song
        super().__init__(content=ft.Container(content=ft.Row(
                    [
                        ft.Image(src=song.cover_art, width=100, height=100, border_radius=15, fit=ft.ImageFit.COVER),
                        ft.Column(controls=[
                            ft.Text(song.name),
                            ft.Text(song.duration),
                            ]
                        ),
                    ],
                ),
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
            ),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25),),
            on_click=lambda e: self.onSongClicked(e, player=player)
        )
        
    def onSongClicked(self, e, player: models.Player):
        queue = models.Queue(song_list=self.songList, curr_index=self.songList.index(self.song))
        player.stop()
        player.change_queue(queue=queue)
        player.play()

class SquareSongWidget(ft.TextButton):
    def __init__(self, song: yt_models.OnlineSong, songList: list[dm.Song], player:models.Player):
        self.song: yt_models.OnlineSong = song
        self.songList: list[dm.Song] = songList
        super().__init__(content=ft.Container(content=ft.Column(
                    [
                        ft.Image(src=song.cover_art, width=150, height=150, border_radius=15, fit=ft.ImageFit.COVER),
                        ft.Column(controls=[
                            ft.Text(song.name, text_align=ft.TextAlign.CENTER, no_wrap=True, overflow=ft.TextOverflow.FADE),
                            ft.Text(song.duration),
                            ]
                        ),
                    ],
                    alignment=ft.alignment.center,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
                alignment=ft.alignment.center,
            ),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25),),
            width=170,
            on_click=lambda e: self.onSongClicked(e, player=player),
        )

    def onSongClicked(self, e, player: models.Player):
        if type(self.song) is yt_models.OnlineSong:
            lib.logger("SquareSongWidget/onSongClicked", f"Clicked on {self.song.id} by {self.song.artist_id}")
            response = yt.getSongUrl(self.song.id)
            if not response.has_error:
                self.song._path = response.url
        queue = models.Queue(song_list=self.songList, curr_index=self.songList.index(self.song))
        player.stop()
        player.change_queue(queue=queue)
        player.play()

class SuggestionsWidget(ft.ListView):
    suggestions: yt_models.GetSuggestionsResponse
    def __init__(self, results: yt_models.GetSuggestionsResponse, player: models.Player):
        self.player = player
        self.suggestions = results
        super().__init__(expand=1)

        artists = HorizontalListView()
        albums = HorizontalListView()
        songs = HorizontalListView()
        
        if len(self.suggestions.songs) > 0:
            self.controls.append(ft.Container(content=ft.Text('Try listening to', font_family='lilitaone', size=40), padding=ft.Padding(top=20, bottom=10, left=55, right=0)))
            for song in self.suggestions.songs:
                songs.append(SquareSongWidget(song=song, songList=self.suggestions.songs, player=self.player))
        self.controls.append(ft.Container(content=songs, bgcolor='#ffffff5', padding=ft.Padding(top=20, bottom=20, left=20, right=20), border_radius=25))

        if len(self.suggestions.albums) > 0:
            self.controls.append(ft.Container(content=ft.Text('Made for you', font_family='lilitaone', size=40), padding=ft.Padding(top=20, bottom=10, left=55, right=0)))
            for album in self.suggestions.albums:
                albums.append(SquareAlbumWidget(album=album))
        self.controls.append(ft.Container(content=albums, bgcolor='#ffffff5', padding=ft.Padding(top=20, bottom=20, left=20, right=20), border_radius=25))

        if len(self.suggestions.artists) > 0:
            self.controls.append(ft.Container(content=ft.Text('Artists you might like', font_family='lilitaone', size=40), padding=ft.Padding(top=20, bottom=10, left=55, right=0)))
            for artist in self.suggestions.artists:
                artists.append(SquareArtistWidget(artist=artist))
        self.controls.append(ft.Container(content=artists, bgcolor='#ffffff5', padding=ft.Padding(top=20, bottom=20, left=20, right=20), border_radius=25))
        
class HorizontalListView(ft.Row):
    listView: ft.ListView
    def __init__(self):
        self.listView = ft.ListView(horizontal=True, expand=1, height=250)
        scrollToLeft = ft.IconButton(icon=ft.icons.ARROW_LEFT, icon_size=30, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25),), width=50, height=50, on_click=self.scrollLeft)
        scrollToRight = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_size=30, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25),), width=50, height=50, on_click=self.scrollRight)
        super().__init__(controls=[scrollToLeft, self.listView, scrollToRight])

    def append(self, item: ft.Control):
        self.listView.controls.append(item)

    def scrollLeft(self, e):
        self.listView.scroll_to(delta=-170, duration=1000)

    def scrollRight(self, e):
        self.listView.scroll_to(delta=170, duration=1000)

class Search_bar_widget(ft.TextField):
    def __init__(self):
        super().__init__()
        self.border_radius=20
        self.bgcolor='FFFFFF2'
        self.hint_text = 'What do you want to listen to?'
        self.height = 50