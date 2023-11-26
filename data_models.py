#!/usr/bin/env /usr/bin/python3
"""
Defines several classes modelling data that will be received from
the C# backend to be used by the Python frontend:

* User -- A class to represent a single User of the application.   
* Content -- Top level class modelling any kind of content an Artist could make.   
* Album : Content -- A collection of Songs.   
* Playlist : Album -- A /mutable/ collection of Songs created by the User.   
* Song : Content -- A single Song.   
* Artist -- An entity that has zero or more Content.   
"""

import lib
import time
from datetime import timedelta
import vlc


class Content:
    """
    Class modelling any form of Content made my an Artist, inherited
    by several other classes.
    """

    name: str
    artist = None
    _path: str


class Song(Content):
    """
    Models a single Song that can be a part of zero or more Albums or
    Playlists, as well as followed by zero or more Users.
    """

    duration: timedelta

    def __init__(self, name: str, artist, path: str, duration: timedelta):
        self.name = name
        self.artist = artist
        self.duration = duration
        self._path = path

    def play(self):
        player = vlc.MediaPlayer(self._path)
        player.play()
        lib.TODO("Song.play()")
        time.sleep(self.duration.total_seconds())


class Album(Content):
    """
    Immutable collection of Songs made by the same Artist and grouped
    togther.

    * name       -- Name of the Album.   
    * arist      -- Name of the Artist that made the Album.   
    * songs      -- List of Songs in the Album.   
    """

    songs: list[Song]

    def __init__(self, name: str, artist, songs: list[Song], path: str):
        self.name = name
        self.artist = artist
        self.songs = songs
        self._path = path


class Playlist(Album):
    """
    Playlist class to be used in the interface between the back- and
    front-ends.

    * name       -- Name of the Playlist.   
    * arist      -- Name of the Artist that made the Playlist.   
    * songs      -- List of Songs in the Playlist.   
    * add_song() -- Adds a Song to the list of Songs.   
    """

    def __init__(self, name: str, path: str, songs: list[Song] = []):
        self.name = name
        self.songs = songs
        self._path = path

    def add_song(self, song: Song):
        self.songs.append(song)
        lib.TODO("Playlist.add_song()")


class Artist:

    name: str
    albums: list[Album]
    songs: list[Song]
    id: str

    def __init__(self,
                 name: str,
                 id: str = "FTC",
                 albums: list[Album] = [],
                 songs: list[Song] = []):
        self.name = name
        self.id = id
        self.albums = albums
        self.songs = songs


class User:
    """
    A User class to model the data for a user of the application.

    * username  -- Personal identifier   
    * playlists -- List of playlists/albums the user has saved   
    * favourites     -- Special playlist of the user’s favourite songs.   
    * followed  -- List of all the artists that the user has followed.   
    """

    username: str
    token: str
    playlists: list[Playlist]
    favourites: Playlist
    followed_artists: list[Artist]
    followed_albums: list[Album]

    def __init__(self, username: str, token: str):
        """
        Initialise a User instance with no playlists, no
        liked/favourited songs and no followed artists.
        """

        self.username = username
        self.token = token
        self.playlists = []
        self.favourites = Playlist("Favourites", "./playlists/favourites")
        self.followed_artists = []
        self.followed_albums = []

    def change_username(self, new_username: str):
        lib.TODO("User.change_username()")
        self.username = new_username

    def like_song(self, song: Song):
        lib.TODO("User.like_song()")
        self.favourites.add_song(song)

    def follow_artist(self, artist: Artist):
        lib.TODO("User.follow_artist()")
        self.followed_artists.append(artist)

    def follow_album(self, album: Album):
        lib.TODO("User.follow_album()")
        self.followed_albums.append(album)

    def create_playlist(self, name: str):
        lib.TODO("User.create_playlist()")
        playlist = Playlist(name, f"./playlists/{name}")
        self.playlists.append(playlist)


if __name__ == "__main__":
    # Testing code:
    # me = User("alchemistsGestalt", "34pgjtlojtnsj598ih/nhdtsprh54plej")
    # mono = Artist("Mono Inc.")
    # heile_segen = Song("Heile, heile Segen", mono, "")
    # teile = Song("Ich teile dich nicht", mono, "")
    # nimmer = Album("Nimmermehr", mono, [heile_segen, teile], "")
    # # These three calls to append (instead of having an Artist method deal
    # # with them) should never happen, this is just here to set up the example.
    # mono.songs.append(heile_segen)
    # mono.songs.append(teile)
    # mono.albums.append(nimmer)
    # me.like_song(heile_segen)
    # me.like_song(teile)
    # me.follow_artist(mono)
    # me.follow_album(nimmer)
    # heile_segen.play()
    # print(me.favourites._path)
    # for song in me.favourites.songs:
    #     print(song.name, song._path)
    # for artist in me.followed_artists:
    #     print(artist.name, artist.id)
    # for album in me.followed_albums:
    #     print(album.name, album._path)
    me = User("alchemistsGestalt", "34pgjtlojtnsj598ih/nhdtsprh54plej")
    asgard = Artist("Old Gods of Asgard")
    control = Song("Take Contol",
                   asgard,
                   "/mnt/c/users/zeinh/Desktop/D/songs/Old Gods of Asgard - Take Control (Lyric Video).mp3",
                   timedelta(minutes=7, seconds=57))
    control.play()
