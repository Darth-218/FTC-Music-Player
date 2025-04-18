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
import ui_builder

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
        self.browseView = ft.Container(content=localfiles.Localclassview,
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

    def __init__(self, artist: yt_models.OnlineArtist, onClick: Callable[[Any], None] = None, albumClick: Callable[[Any], None] = None, viewAllClick: Callable[[Any], None] = None):
        self.onClick = onClick
        self.albumClick = albumClick
        self.viewAllClick = viewAllClick
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
            on_click=self.onArtistClick,
        )

    def onArtistClick(self, e):
        lib.logger("ArtistWidget/on_click", f"Clicked on {self.content.content.controls[1].value}") # Log the click.

        if self.onClick is not None: # If the onClick callback is provided, call it.
            self.onClick(ArtistView(artist=self.artist, albumClick=self.albumClick, viewAllClick=self.viewAllClick)) # Open the artist view.


class SquareArtistWidget(ft.TextButton):
    """A widget for displaying an artist."""

    def __init__(self, artist: yt_models.OnlineArtist, onClick: Callable[[Any], None] = None, albumClick: Callable[[Any], None] = None, viewAllClick: Callable[[Any], None] = None):
        self.artist = artist
        self.onClick = onClick
        self.albumClick = albumClick
        self.viewAllClick = viewAllClick
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
            on_click=self.onArtistClick,
        )

    def onArtistClick(self, e):
        lib.logger("SquareArtistWidget/on_click", f"Clicked on {self.content.content.controls[1].value}") # Log the click.

        if self.onClick is not None: # If the onClick callback is provided, call it.
            self.onClick(ArtistView(artist=self.artist, albumClick=self.albumClick, viewAllClick=self.viewAllClick)) # Open the artist view.


    def onArtistClick(self, e):
        lib.logger("SquareArtistWidget/on_click", f"Clicked on {self.content.content.controls[1].value}") # Log the click.

        if self.onClick is not None: # If the onClick callback is provided, call it.
            self.onClick(ArtistView(artist=self.artist, albumClick=self.albumClick, viewAllClick=self.viewAllClick)) # Open the artist view.


class AlbumWidget(ft.TextButton):
    """A widget for displaying an album."""

    def __init__(self, album: yt_models.OnlineAlbum, onClick: Callable[[Any], None] = None):
        self.onClick = onClick
        self.album = album
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
            on_click=self.onAlbumClick,
        )

    def onAlbumClick(self, e):
        lib.logger("SquareAlbumWidget/on_click", f"Clicked on {self.content.content.controls[1].value}")
        if self.onClick is not None:
            self.onClick(AlbumView(album=self.album))


class SquareAlbumWidget(ft.TextButton):
    """A widget for displaying an album."""

    def __init__(self, album: yt_models.OnlineAlbum, onClick: Callable[[Any], None] = None):
        self.onClick = onClick
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
                        ft.Text(
                            album.artist.name,
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
            self.onClick(AlbumView(album=self.album))


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
                                ft.Text(song.artist.name, text_align=ft.TextAlign.CENTER, no_wrap=True, overflow=ft.TextOverflow.FADE),
                                ft.Text(song.duration, text_align=ft.TextAlign.CENTER, no_wrap=True, overflow=ft.TextOverflow.FADE),
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

        queue = player.Queue(
            song_list=self.songList, curr_index=self.songList.index(self.song)
        ) # The queue to play the song.
        lib.logger("SpuareSongWidget/onSongClicked", f"The first index is {self.songList[0].name}")
        lib.logger("SquareSongWidget/onSongClicked", f"Clicked on index {self.songList.index(self.song)}")

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
        lib.logger("SuggestionsView/getSuggestions", "Getting suggestions")
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
                albums.append(SquareAlbumWidget(album=album, onClick=self.navigator.open))
            
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
                artists.append(SquareArtistWidget(artist=artist, onClick=self.navigator.open, albumClick=self.navigator.open, viewAllClick=self.navigator.open))
            
            finalWidget.controls.append(
                ft.Container(
                    content=artists,
                    bgcolor="#ffffff5",
                    padding=ft.Padding(top=20, bottom=20, left=20, right=20),
                    border_radius=25,
                )
            ) # Add the artists list view to the final widget.
        

        self.content.content = self.navigator # Set the content of the view to the navigator.
        thread = threading.Thread(target=self.navigator.open, args=(finalWidget,)) # Create a thread to open the final widget in the navigator.
        thread.start() # Start the thread.

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
        
        self.navigator = Navigator(player=self.player) # The navigator for navigating between different views.
        finalWidget = ft.ListView(expand=1) # The final widget to display to the user.
        
        artists = HorizontalListView() # The horizontal list view for the artists.
        albums = HorizontalListView() # The horizontal list view for the albums.
        
        for artist in self.results.artists: # For each artist, add it to the artists list view.
            artists.append(SquareArtistWidget(artist=artist, onClick=self.navigator.open, albumClick=self.navigator.open, viewAllClick=self.navigator.open))
        
        for album in self.results.albums: # For each album, add it to the albums list view.
            albums.append(SquareAlbumWidget(album=album, onClick=self.navigator.open))
        
        finalWidget.controls.append(albums) # Add the albums list view to the final widget.
        
        for song in self.results.songs: # For each song, add it to the final widget.
            finalWidget.controls.append(SongWidget(song=song, songList=self.results.songs))
        
        finalWidget.controls.append(artists) # Add the artists list view to the final widget.
        
        self.content.content = self.navigator # Set the content of the view to the navigator.
        thread = threading.Thread(target=self.navigator.open, args=(finalWidget,)) # Create a thread to open the final widget in the navigator.
        thread.start() # Start the thread.

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

    def __init__(self, album: yt_models.OnlineAlbum):
        self.album = album # The album to display.
        self.content = ft.Container(content=ft.ProgressRing(), alignment=ft.alignment.center, expand=True)
        super().__init__(expand=True)
        self.response = None # The API response.

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
        self.content.content = ft.Container(content=ft.ProgressRing(), alignment=ft.alignment.center, expand=True) # Set the content of the view to a loading indicator.

        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.

        if self.response is None or self.response.has_error: # If the songs are not already loaded or there was an error, get the songs from the API.
            self.response = yt.getAlbumSongs(self.album.id) # The API response.
        
        if self.response.has_error: # If there was an error, log it and return.
            lib.logger("AlbumView/getSongs", self.response.error)
            
            while self.page is None: # Wait for the page to be initialised.
                pass

            setattr(self.page.dialog, 'modal', False) # Set the dialog to not be modal.
            setattr(self.page.dialog, 'title', ft.Text('Error!')) # Set the title of the dialog.
            setattr(self.page.dialog,'content', ft.Text(self.response.error)) # Set the content of the dialog.
            setattr(self.page.dialog, 'on_dismiss', self.errorRenderer) # Set the behaviour of the dialog when it is dismissed.
            setattr(self.page.dialog, 'open', True) # Open the dialog.
            self.page.update() # Update the page.
            return
        
        self.album.songs = self.response.songs # Set the songs of the album to the songs from the API.

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
                                                        ft.Text(self.album.artist.name, size=20),
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

        for song in self.response.songs: # For each song, add it to the final widget.
            finalWidget.controls.append(SongWidget(song=song, songList=self.response.songs))

        self.content.content = finalWidget # Set the content of the view to the final widget.

        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.


class ArtistView(ft.UserControl):
    """The view for displaying an artist."""

    def __init__(self, artist: yt_models.OnlineArtist, albumClick: Callable[[Any], None], viewAllClick: Callable[[Any], None]):
        self.albumClick = albumClick
        self.viewAllClick = viewAllClick
        self.artist = artist
        self.content = ft.Container(content=ft.ProgressRing(), alignment=ft.alignment.center, expand=True)
        super().__init__(expand=True)
        self.albumsResponse = None
        self.latestReleaseResponse = None
        self.artistResponse = None

    def errorRenderer(self, e):
        """Renders the content in case of an error."""

        lib.logger("AlbumView/errorRenderer", 'Rendered a retry button')
        self.content.content = ft.Container(content=ft.TextButton(text='retry', 
                                                                on_click=lambda e: self.getArtist()), 
                                            alignment=ft.alignment.center)
        
        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.

    def getArtist(self):
        """Gets the albums for the artist from the API."""

        lib.logger("ArtistView/getArtist", f"Getting artist {self.artist.id}")
        self.content.content = ft.Container(content=ft.ProgressRing(), alignment=ft.alignment.center, expand=True) # Set the content of the view to a loading indicator.

        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.

        if self.albumsResponse is None or self.albumsResponse.has_error: # If the albums are not already loaded or there was an error, get the albums from the API.
            self.albumsResponse = yt.getArtistAlbums(self.artist.id) # The API response.

        if self.albumsResponse.has_error: # If there was an error, log it and return.
            lib.logger("ArtistView/getArtist", "error getting albums: " + self.albumsResponse.error)

            while self.page is None: # Wait for the page to be initialised.
                pass

            setattr(self.page.dialog, 'modal', False) # Set the dialog to not be modal.
            setattr(self.page.dialog, 'title', ft.Text('Error!')) # Set the title of the dialog.
            setattr(self.page.dialog,'content', ft.Text(self.albumsResponse.error)) # Set the content of the dialog.
            setattr(self.page.dialog, 'on_dismiss', self.errorRenderer) # Set the behaviour of the dialog when it is dismissed.
            setattr(self.page.dialog, 'open', True) # Open the dialog.
            self.page.update() # Update the page.
            return
        
        

        if self.latestReleaseResponse is None or self.latestReleaseResponse.has_error:
            self.latestReleaseResponse = yt.getLatestRelease(self.artist.id)

            if self.latestReleaseResponse.has_error:
                lib.logger("ArtistView/getArtist", "error getting latestRelease: " + self.latestReleaseResponse.error)

                while self.page is None: # Wait for the page to be initialised.
                    pass

                setattr(self.page.dialog, 'modal', False) # Set the dialog to not be modal.
                setattr(self.page.dialog, 'title', ft.Text('Error!')) # Set the title of the dialog.
                setattr(self.page.dialog,'content', ft.Text(self.albumsResponse.error)) # Set the content of the dialog.
                setattr(self.page.dialog, 'on_dismiss', self.errorRenderer) # Set the behaviour of the dialog when it is dismissed.
                setattr(self.page.dialog, 'open', True) # Open the dialog.
                self.page.update() # Update the page.
                return
            
            if self.artistResponse is None or self.artistResponse.has_error:
                self.artistResponse = yt.getArtistData(self.artist.id)

                if self.artistResponse.has_error:
                    lib.logger("ArtistView/getArtist", "error getting artistData: " + self.artistResponse.error)

                    while self.page is None: # Wait for the page to be initialised.
                        pass

                    setattr(self.page.dialog, 'modal', False) # Set the dialog to not be modal.
                    setattr(self.page.dialog, 'title', ft.Text('Error!')) # Set the title of the dialog.
                    setattr(self.page.dialog,'content', ft.Text(self.artistResponse.error)) # Set the content of the dialog.
                    setattr(self.page.dialog, 'on_dismiss', self.errorRenderer) # Set the behaviour of the dialog when it is dismissed.
                    setattr(self.page.dialog, 'open', True) # Open the dialog.
                    self.page.update() # Update the page.
                    return

                self.artist = self.artistResponse.artist # Set the artist to the artist from the API.
            
            self.artist.albums = self.albumsResponse.albums # Set the albums of the artist to the albums from the API.
            self.artist.latestRelease = self.latestReleaseResponse.latestRelease # Set the latest release of the artist to the latest release from the API.

        finalWidget = ft.ListView(
            controls=[
                ft.Container(
                    content=
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Image(
                                        src=self.artist.cover_art,
                                        height=250,
                                        width=250,
                                        border_radius=125,
                                        fit=ft.ImageFit.COVER,
                                        ),
                                    border_radius=125,
                                ),
                                ft.Container(
                                    content=
                                        ft.Column(
                                            controls=[
                                                ft.Text(self.artist.name, font_family="lilitaone", size=50),
                                                ft.Row(
                                                    controls=[
                                                        ft.Text(self.artist.subscriberCount, size=20),
                                                        ft.Text(f" ● ", size=20),
                                                        ft.Text(f"{len(self.artist.albums)} albums", size=20),
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

        if len(self.albumsResponse.albums) > 0: # If there are albums to display, display them.
            finalWidget.controls.append(ft.Text("Albums", font_family="lilitaone", size=40)) # Add the title to the final widget.

        albums = HorizontalListView() # The horizontal list view for the albums.

        for album in self.albumsResponse.albums: # For each album, add it to the final widget.
            albums.append(SquareAlbumWidget(album=album, onClick=self.albumClick))

        finalWidget.controls.append(albums) # Add the albums list view to the final widget.

        if len(self.latestReleaseResponse.latestRelease) > 0:
            finalWidget.controls.append(ft.Row(
                controls=[
                    ft.Text("Songs", font_family="lilitaone", size=40),
                    ft.TextButton(text="View all", on_click= lambda e: self.viewAllClick(SongsView(self.artist)))
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )) # Add the title to the final widget.

        for song in self.latestReleaseResponse.latestRelease:
            finalWidget.controls.append(SongWidget(song, self.latestReleaseResponse.latestRelease))

        self.content.content = finalWidget # Set the content of the view to the final widget.

        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.

    def viewAll_Click(self):
        if self.viewAllClick is not None:
            self.viewAllClick(SongsView(self.artist))

    def build(self):
        thread = threading.Thread(target=self.getArtist)
        thread.start()
        return self.content
    

class SongsView(ft.UserControl):
    def __init__(self, artist: yt_models.OnlineArtist):
        self.artist = artist
        self.songsResponse: yt_models.GetArtistSongsResponse = None
        self.content = ft.Container(content=ft.ProgressRing(), alignment=ft.alignment.center, expand=True)
        super().__init__(expand=True)

    def errorRenderer(self, e):
        """Renders the content in case of an error."""

        lib.logger("SongsView/errorRenderer", 'Rendered a retry button')
        self.content.content = ft.Container(content=ft.TextButton(text='retry', 
                                                                on_click=lambda e: self.getSongs()), 
                                            alignment=ft.alignment.center)
        
        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.

    def getSongs(self):
        lib.logger("SongView/getSongs", f"Getting Songs for the artist: {self.artist.name} with id: {self.artist.id}")

        self.content.content = ft.Container(content=ft.ProgressRing(), alignment=ft.alignment.center, expand=True) # Set the content of the view to a loading indicator.

        while self.page is None: # Wait for the page to be initialised.
            pass

        self.update() # Refresh the UI.

        if self.songsResponse is None or self.songsResponse.has_error:
            self.songsResponse = yt.getArtistSongs(self.artist.id)

            if self.songsResponse.has_error:
                lib.logger("SongsView/getSongs", f"error getting songs: {self.songsResponse.error}")

                while self.page is None: # Wait for the page to be initialised.
                    pass

                setattr(self.page.dialog, 'modal', False) # Set the dialog to not be modal.
                setattr(self.page.dialog, 'title', ft.Text('Error!')) # Set the title of the dialog.
                setattr(self.page.dialog,'content', ft.Text(self.songsResponse.error)) # Set the content of the dialog.
                setattr(self.page.dialog, 'on_dismiss', self.errorRenderer) # Set the behaviour of the dialog when it is dismissed.
                setattr(self.page.dialog, 'open', True) # Open the dialog.
                self.page.update() # Update the page.
                return
            
            finalWidget = ft.ListView(controls=[
                ft.Row(controls=[ft.Text("Songs", font_family="lilitaone", size=40)], alignment=ft.MainAxisAlignment.CENTER)
            ])

            for song in self.songsResponse.songs:
                finalWidget.controls.append(SongWidget(song, self.songsResponse.songs))

            self.content.content = finalWidget

            while self.page is None:
                pass

            self.update()

    def build(self):
        thread = threading.Thread(target=self.getSongs)
        thread.start()
        return self.content


class SettingsView(ft.UserControl):

    string_Afifi = ft.Text("""\tWeb-Based Backend Developer
Meet the man that got this team together! Without him, we probably would never
have met each other, and without his powerful C# API, you would never have met
your favourite songs in our app! (unless, of course, you had them downloaded
locally).""", size=15, text_align=ft.TextAlign.CENTER)

    string_zein = ft.Text("""\tData Manager
You're probably wondering what kind of glorious leader could've organised such a
legendary project. Well, you need wonder no more! With about 50 programming
languages under his built--and many more to come!--This fellow will surely leave
a good impression.""", size=15, text_align=ft.TextAlign.CENTER)

    string_yahia = ft.Text("""\t
This man has to go through a perilous adventure every single day, crossing
oceans and fighting *at least* three dragons (not to mention the hordes of their
minions) just to get to his morning lectures from his abode all the way in El
Moqattam.""", size=15, text_align=ft.TextAlign.CENTER)

    string_AbdElmaboud = ft.Text("""\tUX Designer
I'll be honest, I have no idea what a "UX" person does. What I *do* know,
however, is that this guy can and *will* absolutely destroy you if you ever meet
him in the middle lane of a League of Legends match while he's playing Katarina.""", size=15, text_align=ft.TextAlign.CENTER)
    
    string_zein_contributors = ft.Text("""\tTEAM LEADER
We work with a ton of data. From the SearchRequests that get sent to YouTube and
the SearchResults that get sent back,  the Songs, Albums, Artists, and Playlists
that we get from  those SearchResults or from the local files in  the OS, not to
mention  the  player  that actually  plays  the  music,  all  of that  is  data;
therefore, all of that has to pass through Zein.
** Classes:
*** Data:
**** Application
***** Song
A single song, whether from YouTube or the user's file system.
***** Artist
An artist that has made some songs.
***** Album
An album containing songs an artist has made.
***** Playlist
A playist the user has created.
***** User
A user of our application.
**** Web API
***** SearchRequest
A request that will be sent to our API to be eventually sent to YT.
***** SearchResult
The response the API has given, translated from the JSON sent from YT.
*** API
**** Player
The thing that actually plays the music.
**** PlayerState
Enumerates the possible states that the player can be in.
**** VlcMediaPlayer
Implementation of Player. Uses python-vlc to play the music.
**** PlayerWidget
Manages the Player class and provides an interface to the user so they can
interact with it (the bit at the bottom of the screen with the buttons and the
slider).""", size=15, text_align=ft.TextAlign.CENTER)

    string_Afifi_contributors = ft.Text("""There aren't any good Python libraries for communicating with YouTube over
HTTPS, so Afifi made an API in C# that lets us do just that, as well as the
Python API client that lets us use it. He also worked on most of the GUI.""", size=15, text_align=ft.TextAlign.CENTER)

    string_AbdElmaboud_contributors = ft.Text("""Originally was the one responsible for, and who wrote most of, the GUI as we
went from graphics lib to another. We switched from TKInter to customTKInter to
kivy to curses before finally settling on something that worked. That something
was flet, and Adbel-maboud worked on most of the scratched GUI code.""", size=15, text_align=ft.TextAlign.CENTER)

    string_yahia_contributors = ft.Text("""The swiss army knife of our group, he worked on the system for getting songs
from the files local to the user's machine, as well as helping with some of the
UI among other things.""", size=15, text_align=ft.TextAlign.CENTER)

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
        return ft.ListView(controls=[ft.Container(ft.Column(
            [
                ft.Row([
                    ft.Text("Appearance", size=20),
                    ft.Dropdown(
                        width=240,
                        border_color='grey94',
                        hint_text='Choose Your Apperance!',
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
            ),

            ft.Row(
                [
                    ft.OutlinedButton('contributors', on_click=self.open_contributors_popup),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),


        ],
        spacing=40,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        width=800,
        ),
        expand=1,
        alignment=ft.alignment.center,
        )
        ]    
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


    def open_contributors_popup(self, e):
        while self.page is None:
            pass

        setattr(self.page.dialog, 'modal', False)
        setattr(self.page.dialog, 'title', ft.Text('contributors'))
        setattr(self.page.dialog, 'content', ft.ListView(
            [
                ft.Row(controls=[
                    ft.Container(ft.Image('./Assets/Images/ftc.png', width=300, height=300), padding=30),
                    ft.Container(ft.Image('./Assets/Images/ComMusic.png', width=350, height=350), padding=30),
                ], expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text('Ahmed Afifi', size=30, text_align=ft.TextAlign.CENTER),
                    self.string_Afifi_contributors, 
                ft.Text('Zein Hatem Hafez', size=30, text_align=ft.TextAlign.CENTER), 
                    self.string_zein_contributors,
                ft.Text('Yahia Hany Gaber', size=30, text_align=ft.TextAlign.CENTER),
                    self.string_yahia_contributors,
                ft.Text('Ahmed Abdelmaboud', size=30, text_align=ft.TextAlign.CENTER),
                    self.string_AbdElmaboud_contributors,], width=800,))

        setattr(self.page.dialog, 'open', True)

        self.page.update()
        


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

        setattr(self.page.dialog, 'open', True)

        self.page.update()


    def Close_About_us_popup(self, e):
        while self.page is None:
            pass

        setattr(self.page.dialog, 'open', False)
        self.page.update()


    def add_interest(self, e):
        if self.interest.value:
            with open('interest.txt', 'a') as file:
                file.write(self.interest.value + '\n')


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