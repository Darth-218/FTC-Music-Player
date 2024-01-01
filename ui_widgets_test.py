"""This module contains the UI widgets for the app."""

import flet as ft
import api_client.Youtube.api_models as yt_models
import api_client.Youtube.youtube as yt
import data_models as dm
import player
import lib
import config
import localfiles
from typing import Callable, Any
from datetime import timedelta
from threading import Timer
import threading

class Tab():
    """A tab that can be displayed in the tab bar.
    """

    def __init__(self, name: str, content: ft.UserControl):
        self.name = name # The name of the tab
        self.content = content # The content of the tab

class Navigator(ft.UserControl):
    """A navigator for navigating between different views."""

    def __init__(self, player: player.Player):
        self.player = player # The player to play the songs.
        self.content = ft.Container(expand=True) # The content of the navigator.
        self.navigator = ft.Column(controls=[
                        ft.Container(content=ft.IconButton(icon=ft.icons.ARROW_BACK_ROUNDED, 
                            on_click=lambda e: self.back()
                        ), 
                        alignment=ft.alignment.top_left, 
                        padding=ft.Padding(20, 20, 0, 0), 
                        ), # The back button.
                    self.content]) # The navigator.

        self.history = [] # The history of the navigator.
        super().__init__(expand=True)

    def build(self):
        return self.navigator # Return the navigator.

    def open(self, view: Any):
        """Opens a view in the navigator."""
        lib.logger("Navigator/open", f"Opened {view}")

        self.navigator.controls[1] = view # Set the content of the navigator to the view.
        self.history.append(view)

        while self.page is None:
            pass

        self.update() # Refresh the UI.

    def back(self):
        """Goes back to the previous view in the navigator."""
        if len(self.history) <= 1:
            lib.logger("Navigator/back", "Cannot go back any further")
            return
        
        lib.logger("Navigator/back", f"Going back from {self.navigator.controls[1]} to {self.history[-2]}")

        self.history.pop() # Remove the current view from the history.
        self.navigator.controls[1] = self.history[-1] # Set the content of the navigator to the previous view.
        self.update() # Refresh the UI.

class TabView(ft.UserControl):
    """The view for the tab bar. It is responsible for displaying the
    different tabs to the user.
    """

    def __init__(self, tabs: list[Tab]):
        self.tabs = tabs # The tabs to display
        self.selectedTabIndex = 0 # The index of the selected tab
        self.selectedTab = ft.Container(bgcolor = '#FFFFFF3', 
                                        content=tabs[0].content, 
                                        expand=True, 
                                        border_radius= 30,
                                        padding=ft.Padding(20, 0, 20, 0)) # The content of the selected tab
        super().__init__(expand=True)

    def build(self):
        return ft.Container(expand=True,
            content=ft.Row(controls=[
                ft.Container(bgcolor= "#FFFFFF3",
                            border_radius= 30,
                            padding= ft.Padding(20, 20, 20, 0),
                            width=200,
                            content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                        controls=[
                            ft.ElevatedButton(
                                text=tab.name,
                                data=tab,
                                on_click=lambda e: self.onTabClicked(e), 
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=25)), 
                                width=150, height=50)
                            for i, tab in enumerate(self.tabs)
                        ]),),
                self.selectedTab
            ])
        )
    
    def onTabClicked(self, e):
        """Called when a tab is clicked. It updates the selected tab and refreshes the UI.
        """

        tab = e.control.data # The tab that was clicked
        lib.logger("TabView/onTabClicked", f"Clicked on {tab.name} tab with index {self.tabs.index(tab)}")
        self.selectedTabIndex = self.tabs.index(tab) # Update the selected tab index
        self.selectedTab.content = self.tabs[self.selectedTabIndex].content # Update the selected tab content
        self.update() # Refresh the UI


class Home(ft.UserControl):
    """The view for the home tab. It is responsible for displaying the
    different views to the user.
    """

    def __init__(self, player: player.Player):
        self.player = player
        self.suggestionsView = ft.Container(content=SuggestionsView(player=player),
                                        expand=True,
                                        alignment=ft.alignment.center,) # The view for the suggestions tab.
        self.searchView = ft.Container(content=SearchView(player=player), 
                                    expand=True, 
                                    alignment=ft.alignment.center, 
                                    padding=ft.Padding(0, 20, 0, 0)) # The view for the search tab.
        self.browseView = ft.Container(content=localfiles.LocalView(),
                                    expand=True,
                                    alignment=ft.alignment.center,) # The view for the browse tab.
        self.settingsView = ft.Container(content=SettingsView(),
                                    expand=True,
                                    alignment=ft.alignment.center,) # The view for the settings tab.
        super().__init__(expand=True)

    def build(self):
        return TabView(tabs=[
            Tab("Home", self.suggestionsView),
            Tab("Search", self.searchView),
            Tab("Browse", self.browseView),
            Tab("Settings", self.settingsView)
        ])


class ArtistWidget(ft.TextButton):
    """A widget for displaying an artist."""

    def __init__(self, artist: yt_models.OnlineArtist):
        super().__init__(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Image(
                            src=artist.cover_art,
                            width=100,
                            height=100,
                            border_radius=15,
                            fit=ft.ImageFit.COVER,
                        ),
                        ft.Text(artist.name),
                    ],
                ),
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=25),
            ),
        )


class SquareArtistWidget(ft.TextButton):
    """A widget for displaying an artist."""

    def __init__(self, artist: yt_models.OnlineArtist):
        super().__init__(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src=artist.cover_art,
                            width=150,
                            height=150,
                            border_radius=75,
                            fit=ft.ImageFit.COVER,
                        ),
                        ft.Text(
                            artist.name,
                            text_align=ft.TextAlign.CENTER,
                            no_wrap=True,
                            overflow=ft.TextOverflow.FADE,
                        ),
                    ],
                    alignment=ft.alignment.center,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
                alignment=ft.alignment.center,
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=25),
            ),
            width=170,
        )


class AlbumWidget(ft.TextButton):
    """A widget for displaying an album."""

    def __init__(self, album: yt_models.OnlineAlbum):
        super().__init__(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Image(
                            src=album.cover_art,
                            width=100,
                            height=100,
                            border_radius=15,
                            fit=ft.ImageFit.COVER,
                        ),
                        ft.Text(album.name),
                    ],
                ),
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=25),
            ),
        )


class SquareAlbumWidget(ft.TextButton):
    """A widget for displaying an album."""

    def __init__(self, album: yt_models.OnlineAlbum, player, onClick: Callable[[Any], None] = None):
        self.onClick = onClick
        self.player = player
        self.album = album
        super().__init__(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src=album.cover_art,
                            width=150,
                            height=150,
                            border_radius=15,
                            fit=ft.ImageFit.COVER,
                        ),
                        ft.Text(
                            album.name,
                            text_align=ft.TextAlign.CENTER,
                            no_wrap=True,
                            overflow=ft.TextOverflow.FADE,
                        ),
                    ],
                    alignment=ft.alignment.center,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
                alignment=ft.alignment.center,
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=25),
            ),
            width=170,
            on_click=self.onAlbumClick,
        )

    def onAlbumClick(self, e):
        lib.logger("SquareAlbumWidget/on_click", f"Clicked on {self.content.content.controls[1].value}")
        if self.onClick is not None:
            self.onClick(AlbumView(album=self.album, player=self.player))


class SongWidget(ft.TextButton):
    """A widget for displaying a song."""

    def __init__(self, song: dm.Song, songList: list[dm.Song]):
        self.songList: list[dm.Song] = songList
        self.song: yt_models.OnlineSong = song
        super().__init__(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Image(
                            src=song.cover_art,
                            width=100,
                            height=100,
                            border_radius=15,
                            fit=ft.ImageFit.COVER,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(song.name),
                                ft.Text(song.duration),
                            ]
                        ),
                    ],
                ),
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=25),
            ),
            on_click=lambda e: self.onSongClicked(e), # Call onSongClicked when the song is clicked.
        )

    def onSongClicked(self, e):
        """Called when the song is clicked. It plays the song."""

        # if type(self.song) is yt_models.OnlineSong: # If the song is an online song, get the URL for the song.
        #     lib.logger(
        #         "SquareSongWidget/onSongClicked",
        #         f"Clicked on {self.song.id} by {self.song.artist_id}",
        #     )

        #     response = yt.getSongUrl(self.song.id) # The response from the API.
            
        #     if not response.has_error: # If there was no error, set the path of the song to the URL.
        #         self.song._path = response.url
            
        queue = player.Queue(
            song_list=self.songList, curr_index=self.songList.index(self.song)
        ) # The queue to play the song.

        while self.page is None:
            pass
        while self.page.bottom_appbar is None:
            pass
        self.page.bottom_appbar.content.player.change_queue(queue=queue) # Change the queue of the player.
        self.page.bottom_appbar.content.play() # Play the song in the player widget.


class SquareSongWidget(ft.TextButton):
    """A widget for displaying a song."""

    def __init__(
        self, song: yt_models.OnlineSong, songList: list[dm.Song]
    ):
        self.song: yt_models.OnlineSong = song
        self.songList: list[dm.Song] = songList
        super().__init__(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src=song.cover_art,
                            width=150,
                            height=150,
                            border_radius=15,
                            fit=ft.ImageFit.COVER,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    song.name,
                                    text_align=ft.TextAlign.CENTER,
                                    no_wrap=True,
                                    overflow=ft.TextOverflow.FADE,
                                ),
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
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=25),
            ),
            width=170,
            on_click=lambda e: self.onSongClicked(e), # Call onSongClicked when the song is clicked.
        )

    def onSongClicked(self, e):
        """Called when the song is clicked. It plays the song."""

        # if type(self.song) is yt_models.OnlineSong: # If the song is an online song, get the URL for the song.
        #     lib.logger(
        #         "SquareSongWidget/onSongClicked",
        #         f"Clicked on {self.song.id} by {self.song.artist_id}",
        #     )

        #     response = yt.getSongUrl(self.song.id) # The response from the API.

        #     if not response.has_error: # If there was no error, set the path of the song to the URL.
        #         self.song._path = response.url
            
        queue = player.Queue(
            song_list=self.songList, curr_index=self.songList.index(self.song)
        ) # The queue to play the song.

        while self.page is None: # Wait for the page to be initialised.
            pass
        while self.page.bottom_appbar is None: # Wait for the bottom app bar to be initialised.
            pass
        self.page.bottom_appbar.content.player.change_queue(queue=queue) # Change the queue of the player.
        self.page.bottom_appbar.content.play() # Play the song in the player widget.


class HorizontalListView(ft.Row):
    """A horizontal list view for displaying a list of items."""

    listView: ft.ListView # The list view to display the items.

    def __init__(self):
        self.listView = ft.ListView(horizontal=True, expand=1, height=250) # Initialise the list view.

        scrollToLeft = ft.IconButton(
            icon=ft.icons.ARROW_LEFT,
            icon_size=30,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=25),
            ),
            width=50,
            height=50,
            on_click=self.scrollLeft,
        ) # The button to scroll to the left.

        scrollToRight = ft.IconButton(
            icon=ft.icons.ARROW_RIGHT,
            icon_size=30,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=25),
            ),
            width=50,
            height=50,
            on_click=self.scrollRight,
        ) # The button to scroll to the right.

        super().__init__(controls=[scrollToLeft, self.listView, scrollToRight])

    def append(self, item: ft.Control):
        """Appends an item to the list view."""

        self.listView.controls.append(item)

    def scrollLeft(self, e):
        """Scrolls the list view to the left."""

        self.listView.scroll_to(delta=-510, duration=500)

    def scrollRight(self, e):
        """Scrolls the list view to the right."""

        self.listView.scroll_to(delta=510, duration=500)


class Search_bar_widget(ft.TextField):
    """A search bar widget for searching for songs, artists and albums."""

    def __init__(self, onSubmit: Callable[[str], None], query=None):
        super().__init__()
        self.border_radius = 20
        self.bgcolor = "FFFFFF2"
        self.hint_text = "What do you want to listen to?"
        self.height = 50
        self.on_submit = lambda e: onSubmit(self.value)
        if query != None: # If a query is provided, set the value of the search bar to the query.
            self.value = query


class SuggestionsView(ft.UserControl):
    """The view for the suggestions tab. It is responsible for displaying
    the suggestions to the user.
    """
    suggestions: yt_models.GetSuggestionsResponse = None # The suggestions API response.
    content: ft.Container = ft.Container(
                    content=ft.ProgressRing(),
                    alignment=ft.alignment.center,
                    expand=True,
                ) # The content of the view.
    navigator: Navigator = None # The navigator for navigating between different views.

    def __init__ (self, player: player.Player):
        self.player = player
        super().__init__(expand=True)

    def errorRenderer(self, e):
        """Renders the content in case of an error."""

        lib.logger("SuggestionsView/errorRenderer", 'Rendered a retry button')
        self.content.content = ft.Container(content=ft.TextButton(text='retry', 
                                                                on_click=lambda e: self.getSuggestions()), 
                                            alignment=ft.alignment.center) # Add a retry button in the center of the screen that invokes the getSuggestions method again.
        self.update() # Refresh the UI.

    def getSuggestions(self, forceRefresh=False):
        """Gets the suggestions from the API and displays them to the user."""

        if self.navigator is not None:
            self.content.content = self.navigator # Set the content of the view to the navigator.

            while self.page is None:
                pass

            self.update() # Refresh the UI.
            return

        self.content.content = ft.Container(
                    content=ft.ProgressRing(),
                    alignment=ft.alignment.center,
                    expand=True,
                ) # Set the content of the view to a loading indicator.

        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.

        lib.logger("SuggestionsView/getSuggestions", "Getting suggestions")
        if forceRefresh or self.suggestions is None or self.suggestions.has_error: # If the suggestions are not already loaded or there was an error, get the suggestions from the API.
            request = yt_models.GetSuggestionsRequest(config.numberOfArtistsPerInterest, 
                                                    config.numberOfAlbumsPerInterest, 
                                                    config.numberOfSongsPerInterest, 
                                                    config.interests) # The request to get the suggestions.
            self.suggestions = yt.getSuggestions(request) # The suggestions API response.

        if self.suggestions.has_error: # If there was an error, log it and return.
            lib.logger("SuggestionsView/getSuggestions", self.suggestions.error)

            while self.page is None: # Wait for the page to be initialised.
                pass

            setattr(self.page.dialog, 'title', ft.Text('Error!')) # Set the title of the dialog.
            setattr(self.page.dialog,'content', ft.Text(self.suggestions.error)) # Set the content of the dialog.
            setattr(self.page.dialog, 'on_dismiss', self.errorRenderer) # Set the behaviour of the dialog when it is dismissed.
            setattr(self.page.dialog, 'open', True) # Open the dialog.
            self.page.update() # Update the page.
            return
        
        self.navigator = Navigator(player=self.player) # The navigator for navigating between different views.
        finalWidget = ft.ListView(expand=1) # The final widget to display to the user.

        artists = HorizontalListView() # The horizontal list view for the artists.
        albums = HorizontalListView() # The horizontal list view for the albums.
        songs = HorizontalListView() # The horizontal list view for the songs.

        if len(self.suggestions.songs) > 0: # If there are songs to display, display them.
            finalWidget.controls.append(
                ft.Container(
                    content=ft.Text(
                        "Try listening to", font_family="lilitaone", size=40
                    ),
                    padding=ft.Padding(top=20, bottom=10, left=55, right=0),
                )
            ) # Add the title to the final widget.

            for song in self.suggestions.songs: # For each song, add it to the songs list view.
                songs.append(
                    SquareSongWidget(
                        song=song, songList=self.suggestions.songs
                    )
                )
            
            finalWidget.controls.append(
                ft.Container(
                    content=songs,
                    bgcolor="#ffffff5",
                    padding=ft.Padding(top=20, bottom=20, left=20, right=20),
                    border_radius=25,
                )
            ) # Add the songs list view to the final widget.

        if len(self.suggestions.albums) > 0: # If there are albums to display, display them.
            finalWidget.controls.append(
                ft.Container(
                    content=ft.Text("Made for you", font_family="lilitaone", size=40),
                    padding=ft.Padding(top=20, bottom=10, left=55, right=0),
                )
            ) # Add the title to the final widget.

            for album in self.suggestions.albums: # For each album, add it to the albums list view.
                albums.append(SquareAlbumWidget(album=album, player=self.player, onClick=self.navigator.open))
            
            finalWidget.controls.append(
                ft.Container(
                    content=albums,
                    bgcolor="#ffffff5",
                    padding=ft.Padding(top=20, bottom=20, left=20, right=20),
                    border_radius=25,
                )
            ) # Add the albums list view to the final widget.

        if len(self.suggestions.artists) > 0: # If there are artists to display, display them.
            finalWidget.controls.append(
                ft.Container(
                    content=ft.Text(
                        "Artists you might like", font_family="lilitaone", size=40
                    ),
                    padding=ft.Padding(top=20, bottom=10, left=55, right=0),
                )
            ) # Add the title to the final widget.

            for artist in self.suggestions.artists: # For each artist, add it to the artists list view.
                artists.append(SquareArtistWidget(artist=artist))
            
            finalWidget.controls.append(
                ft.Container(
                    content=artists,
                    bgcolor="#ffffff5",
                    padding=ft.Padding(top=20, bottom=20, left=20, right=20),
                    border_radius=25,
                )
            ) # Add the artists list view to the final widget.
        

        self.content.content = self.navigator # Set the content of the view to the navigator.
        # navigator.open(finalWidget) # Open the final widget in the navigator.
        thread = threading.Thread(target=self.navigator.open, args=(finalWidget,))
        thread.start()
        # self.content.content = finalWidget

        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.

        lib.logger("SuggestionsView/getSuggestions", "Got suggestions")


    def refresh(self):
        self.content.content = ft.Container(
                    content=ft.ProgressRing(),
                    alignment=ft.alignment.center,
                    expand=True,
                )
        self.update()
        thread = threading.Thread(target=self.getSuggestions, args=(True))
        thread.start()

    def build(self):
        thread = threading.Thread(target=self.getSuggestions)
        thread.start()
        return self.content


class SearchResultsView(ft.UserControl):
    """Responsible for displaying the search results to the user."""

    content = ft.Container(content=ft.Container(
                    content=ft.ProgressRing(),
                    alignment=ft.alignment.center,
                    expand=True,
                ), expand=True) # The content of the view.
    results: yt_models.SearchResponse = None # The search API response.

    def __init__(self, player: player.Player, query: str):
        self.query = query # The query to search for.
        self.player = player # The player to play the songs.
        super().__init__(expand=True)

    def errorRenderer(self, e):
        """Renders the content in case of an error."""

        lib.logger("SearchResultsView/errorRenderer", 'Rendered a retry button')
        self.content.content = ft.Container(content=ft.TextButton(text='retry', 
                                                                on_click=lambda e: self.search()), 
                                            alignment=ft.alignment.center) # Add a retry button in the center of the screen that invokes the search method again.
        self.update() # Refresh the UI.

    def search(self):
        """Gets the search results from the API and displays them to the user."""
        lib.logger("SearchView/search", f"Searching for {self.query}")

        self.content.content = ft.Container(
                    content=ft.ProgressRing(),
                    alignment=ft.alignment.center,
                    expand=True,
                ) # Set the content of the view to a loading indicator.
        
        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.

        request = yt_models.SearchRequest(query=self.query, 
                                        artist_count=config.numberOfSearchArtists, 
                                        album_count=config.numberOfSearchAlbums, 
                                        song_count=config.numberOfSearchSongs) # The request to search for the query.
        
        self.results = yt.search(request) # The search API response.

        if self.results.has_error: # If there was an error, log it and return.
            lib.logger("SearchView/search", self.results.error)

            while self.page is None: # Wait for the page to be initialised.
                pass

            setattr(self.page.dialog, 'modal', False) # Set the dialog to not be modal.
            setattr(self.page.dialog, 'title', ft.Text('Error!')) # Set the title of the dialog.
            setattr(self.page.dialog,'content', ft.Text(self.results.error)) # Set the content of the dialog.
            setattr(self.page.dialog, 'on_dismiss', self.errorRenderer) # Set the behaviour of the dialog when it is dismissed.
            setattr(self.page.dialog, 'open', True) # Open the dialog.
            self.page.update() # Update the page.
            return
        
        finalWidget = ft.ListView(expand=1) # The final widget to display to the user.
        
        artists = HorizontalListView() # The horizontal list view for the artists.
        albums = HorizontalListView() # The horizontal list view for the albums.
        
        for artist in self.results.artists: # For each artist, add it to the artists list view.
            artists.append(SquareArtistWidget(artist=artist))
        
        for album in self.results.albums: # For each album, add it to the albums list view.
            albums.append(SquareAlbumWidget(album=album, player=self.player))
        
        finalWidget.controls.append(albums) # Add the albums list view to the final widget.
        
        for song in self.results.songs: # For each song, add it to the final widget.
            finalWidget.controls.append(SongWidget(song=song, songList=self.results.songs))
        
        finalWidget.controls.append(artists) # Add the artists list view to the final widget.
        
        self.content.content = finalWidget # Set the content of the view to the final widget.

        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.
        
    def build(self):
        if self.results is None or self.results.has_error:
            thread = threading.Thread(target=self.search) # Create a thread to search for the query.
            thread.start() # Start the thread.
        return self.content


class SearchView(ft.UserControl):
    """The view for the search tab. It is responsible for displaying the
    search results to the user.
    """

    def __init__(self, player: player.Player):
        super().__init__(expand=True)
        self.player = player # The player to play the songs.
        self.searchField: Search_bar_widget = Search_bar_widget(onSubmit=self.onSearch) # The search bar widget.
        self.results: ft.Container = ft.Container(expand=True) # The search results view.
        self.content = ft.Container(expand=True, content=ft.Column(controls=[
            self.searchField,
            self.results
        ])) # The content of the view.

    def build(self):
        return self.content
    
    def onSearch(self, query):
        self.results.content = SearchResultsView(player=self.player, query=query) # Set the content of the view to the search results view.

        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.


class PlayerWidget(ft.UserControl):
    """A Player widget at the bottom of the screen having buttons
    for playing/pausing, skipping forwards and backwards, shuffling etc.
    as well as a slider for the current song.
    """

    btn_shuffle: ft.IconButton
    btn_prev: ft.IconButton
    btn_play_pause: ft.IconButton
    btn_next: ft.IconButton
    btn_repeat: ft.IconButton
    slider: ft.Slider

    def __init__(self, player: player.Player):
        super().__init__()
        self.player = player

    def build(self):
        self.bgcolor = "#000000"
        self.padding = ft.Padding(0, 0, 0, 10)

        self.btn_shuffle = ft.IconButton(icon=ft.icons.SHUFFLE, icon_size=40)
        self.btn_prev = ft.IconButton(
            icon=ft.icons.SKIP_PREVIOUS,
            on_click=lambda e: self.player.prev(),
            icon_size=40,
        )
        self.btn_play_pause = ft.IconButton(
            icon=ft.icons.PLAY_CIRCLE, on_click=self.play_pause, icon_size=40
        )
        self.btn_next = ft.IconButton(
            icon=ft.icons.SKIP_NEXT, on_click=lambda e: self.player.next(), icon_size=40
        )
        self.btn_repeat = ft.IconButton(icon=ft.icons.REPEAT, icon_size=40)
        self.slider = ft.Slider(min=0.0, max=1.0, on_change=self.slider_seek, value=0.0)
        return ft.Container(bgcolor="#000000", content=ft.Column(
            controls=[
                ft.Container(self.slider, width=500, alignment=ft.alignment.center),
                ft.Row(
                    controls=[
                        self.btn_shuffle,
                        self.btn_prev,
                        self.btn_play_pause,
                        self.btn_next,
                        self.btn_repeat,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.alignment.center,
                    expand=False,
                ),
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.alignment.center,
        ))
    def play_pause(self, event=None) -> None:
        """Toggles the player's currently paused/resumed state."""
        match self.player.state:
            case player.PlayerState.playing:
                self.player.pause()
                setattr(self.btn_play_pause, "icon", ft.icons.PLAY_CIRCLE)
            case player.PlayerState.paused:
                self.player.pause()
                setattr(self.btn_play_pause, "icon", ft.icons.PAUSE_CIRCLE)
        self.update()
    def play(self):
        setattr(self.btn_play_pause, "icon", ft.icons.PAUSE_CIRCLE)
        self.update_slider()
        self.player.play()

    def pause(self):
        self.play_pause()

    def update_slider(self):
        Timer(0.2, self.update_slider).start()
        current_position = self.player.getpos()
        if current_position == self.slider.value:
            return
        setattr(self.slider, "value", current_position)
        current_time_in_ms = self.player.gettime()
        current_time = timedelta(milliseconds=current_time_in_ms)
        lib.logger("PlayerWidget/update_slider", f"Updating to {current_time}")
        self.update()

    def slider_seek(self, e):
        new_val = e.control.value
        self.player.seekpos(new_val)
        current_time_in_ms = self.player.gettime()
        current_time = timedelta(milliseconds=current_time_in_ms)
        lib.logger("PlayerWidget/slider_seek", f"Moved to {current_time}")


class AlbumView(ft.UserControl):
    """The view for displaying an album."""

    def __init__(self, album: yt_models.OnlineAlbum, player: player.Player):
        self.album = album # The album to display.
        self.player = player # The player to play the songs.
        self.content = ft.Container(content=ft.ProgressRing(), alignment=ft.alignment.center, expand=True)
        super().__init__(expand=True)

    def build(self):
        thread = threading.Thread(target=self.getSongs) # Create a thread to get the songs for the album.
        thread.start() # Start the thread.
        return self.content # Return the content of the view.
    
    def errorRenderer(self, e):
        """Renders the content in case of an error."""

        lib.logger("AlbumView/errorRenderer", 'Rendered a retry button')
        self.content.content = ft.Container(content=ft.TextButton(text='retry', 
                                                                on_click=lambda e: self.getSongs()), 
                                            alignment=ft.alignment.center)
        
        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.

    def getSongs(self):
        """Gets the songs for the album from the API."""

        lib.logger("AlbumView/getSongs", f"Getting songs for {self.album.id}")
        self.content.content = ft.Container(content=ft.ProgressRing(), alignment=ft.alignment.center, expand=True)

        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.

        response = yt.getAlbumSongs(self.album.id)
        
        if response.has_error: # If there was an error, log it and return.
            lib.logger("AlbumView/getSongs", response.error)
            
            while self.page is None: # Wait for the page to be initialised.
                pass

            setattr(self.page.dialog, 'modal', False) # Set the dialog to not be modal.
            setattr(self.page.dialog, 'title', ft.Text('Error!')) # Set the title of the dialog.
            setattr(self.page.dialog,'content', ft.Text(response.error)) # Set the content of the dialog.
            setattr(self.page.dialog, 'on_dismiss', self.errorRenderer) # Set the behaviour of the dialog when it is dismissed.
            setattr(self.page.dialog, 'open', True) # Open the dialog.
            self.page.update() # Update the page.
            return
        
        self.album.songs = response.songs # Set the songs of the album to the songs from the API.

        finalWidget = ft.ListView(
            controls=[
                ft.Container(
                    content=
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Image(
                                        src=self.album.cover_art,
                                        height=250,
                                        width=250,
                                        border_radius=25,
                                        fit=ft.ImageFit.COVER,
                                        ),
                                    border_radius=25,
                                ),
                                ft.Container(
                                    content=
                                        ft.Column(
                                            controls=[
                                                ft.Text(self.album.name, font_family="lilitaone", size=50),
                                                ft.Row(
                                                    controls=[
                                                        ft.Text(self.album.artist, size=20),
                                                        ft.Text(f" ● ", size=20),
                                                        ft.Text(f"{len(self.album.songs)} songs", size=20),
                                                    ]
                                                ),
                                            ],
                                            alignment=ft.alignment.center, 
                                            horizontal_alignment=ft.CrossAxisAlignment.START
                                        ),
                                        padding=ft.Padding(top=20, bottom=20, left=20, right=20),
                                )
                            ]
                        ),
                    padding=ft.Padding(top=0, bottom=20, left=0, right=0),
                ),
            ]
        ) # The final widget to display to the user.

        for song in response.songs: # For each song, add it to the final widget.
            finalWidget.controls.append(SongWidget(song=song, songList=response.songs))

        self.content.content = finalWidget # Set the content of the view to the final widget.

        while self.page is None:
            pass

        self.update() # Refresh the UI.


class SettingsView(ft.UserControl):

    string_Afifi = ft.Text("""\tMeet the former leader of the team while we were making the best
presentation the university has ever seen (and will ever see, unless we
decide to make another one in the future)! This guy has made his very own
music streaming mobile application in dart, not to mention countless
arduino projects in the microprocessor's modified C++; from an AC remote
controllable from your laptop to hacking the Pentagon (one of these is
true, not sure which one), this dude's got you covered.""", size=15, text_align=ft.TextAlign.CENTER)

    string_zein = ft.Text("""\tIt is never very hard to find this guy, all you have to do is look for
someone with impeccable fashion sense and a great hat. From Magic: the
Gathering to YuGiOh! to Flesh and Blood to any
variant of  he'll dominate you in any card game you
challenge him at. He's also proficient in many languages, including
Python, C#, C++, Rust, Haskell, and Uiua; not to mention human languages.""", size=15, text_align=ft.TextAlign.CENTER)

    string_yahia = ft.Text("""\tComing all the way from the most expensive city in (the Egyptian version
of) Monopoly, el-Moqattam, our team leader has absolutely no fear. Either that
or he's suicidal. I'm not sure which. What I do know, however,
is that he's made multiple projects in Python before.""", size=15, text_align=ft.TextAlign.CENTER)

    string_AbdElmaboud = ft.Text("""\tHe's completely unbeatable in League of Legends and Elden Ring, and he's
won a free ticket to Sa'yet el Sāwi by just being so damn awesome.
Fun fact: he went to the same school as our very own Ahmed Mohamed Afifi!""", size=15, text_align=ft.TextAlign.CENTER)

    def __init__(self):
        super().__init__()
        self.numberOfArtistsPerInterest = ft.TextField(width=120, border_color='grey94')

        self.numberOfAlbumsPerInterest = ft.TextField(width=120, border_color='grey94')

        self.numberOfSongsPerInterest = ft.TextField(width=120, border_color='grey94')

        self.numberOfSearchArtists = ft.TextField(width=120, border_color='grey94')

        self.numberOfSearchAlbums = ft.TextField(width=120, border_color='grey94')

        self.numberOfSearchSongs = ft.TextField(width=120, border_color='grey94')

        self.interest = ft.TextField()

    def build(self):
        return ft.Container(ft.Column(
            [
                ft.Row([
                    ft.Text("Appearance", size=20),
                    ft.Dropdown(
                        width=125,
                        border_color='grey94',
                        options=[
                            ft.dropdown.Option('Light mode'),
                            ft.dropdown.Option('Dark mode'),
                ],
                ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),

            
            ft.Row(
                [
                    ft.Text('number Of Artists Per Interest', size=20),
                    self.numberOfArtistsPerInterest,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.Text('number Of Albums Per Interest', size=20),
                    self.numberOfAlbumsPerInterest,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.Text('number Of Songs Per Interest', size=20),
                    self.numberOfSongsPerInterest,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.Text('number Of Search Artists', size=20),
                    self.numberOfSearchArtists,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.Text('number Of Search Albums', size=20),
                    self.numberOfSearchAlbums,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.Text('number Of Search Songs', size=20),
                    self.numberOfSearchSongs,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.OutlinedButton('Save', width=120, on_click=self.on_save),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.OutlinedButton("Add interest", on_click=self.open_dialouge),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.OutlinedButton('About Us', on_click=self.Open_About_us_popup),
                    
                    
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )


        ],
        spacing=40,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        width=800,
        ),
        expand=1,
        alignment=ft.alignment.center,
        )
    
    def on_save(self, e):

        if self.numberOfArtistsPerInterest.value:
            config.numberOfArtistsPerInterest = self.numberOfArtistsPerInterest.value

        if self.numberOfAlbumsPerInterest.value:
            config.numberOfAlbumsPerInterest = self.numberOfAlbumsPerInterest.value

        if self.numberOfSongsPerInterest.value:
            config.numberOfSongsPerInterest = self.numberOfSongsPerInterest.value

        if self.numberOfSearchArtists.value:
            config.numberOfSearchArtists = self.numberOfSearchArtists.value

        if self.numberOfSearchAlbums.value:
            config.numberOfSearchAlbums = self.numberOfSearchAlbums.value

        if self.numberOfSearchSongs.value:
            config.numberOfSearchSongs = self.numberOfSearchSongs.value


    def Open_About_us_popup(self, e):
        while self.page is None:
            pass

        setattr(self.page.dialog, 'modal', False)
        setattr(self.page.dialog, 'title', ft.Text('About Us'))
        setattr(self.page.dialog, 'content', ft.ListView(
            [
                ft.Row(controls=[
                    ft.Container(ft.Image('./Assets/Images/ftc.png', width=300, height=300), padding=30),
                    ft.Container(ft.Image('./Assets/Images/ComMusic.png', width=350, height=350), padding=30),
                ], expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text('Ahmed Afifi', size=30, text_align=ft.TextAlign.CENTER),
                    self.string_Afifi, 
                ft.Text('Zein Hatem Hafez', size=30, text_align=ft.TextAlign.CENTER), 
                    self.string_zein,
                ft.Text('Yahia Hany Gaber', size=30, text_align=ft.TextAlign.CENTER),
                    self.string_yahia,
                ft.Text('Ahmed Abdelmaboud', size=30, text_align=ft.TextAlign.CENTER),
                    self.string_AbdElmaboud,], width=800,))
        # setattr(self.page.dialog, 'actions', [ft.ElevatedButton('Close', on_click=self.Close_About_us_popup)])
        setattr(self.page.dialog, 'open', True)

        self.page.update()


    def Close_About_us_popup(self, e):
        while self.page is None:
            pass

        setattr(self.page.dialog, 'open', False)
        self.page.update()


    def add_interest(self, e):
        if self.interest.value:
            if config.interests2 == '':
                config.interests2 += f'{self.interest.value}--)0'
            else:
                config.interests2 += f'|*|{self.interest.value}--)0'
            while self.page is None:
                pass
            setattr(self.page.dialog, 'open', False)
            self.page.update()
            print(config.interests2)


    def close_popup(self, e):
            setattr(self.page.dialog, 'open', False)
            self.page.update()


    def open_dialouge(self, e):
        while self.page is None:
            pass

        setattr(self.page.dialog, 'modal', True)
        setattr(self.page.dialog, 'title', ft.Text('Add Interest'))
        setattr(self.page.dialog, 'content', self.interest)
        setattr(self.page.dialog, 'actions', [ft.ElevatedButton('Add', on_click=self.add_interest), ft.ElevatedButton('Close', on_click=self.close_popup)])
        setattr(self.page.dialog, 'open', True)

        self.page.update()
