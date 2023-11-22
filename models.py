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


class Content:
    """
    Class modelling any form of Content made my an Artist, inherited
    by several other classes.
    """

    name: str
    artist = None


class Song(Content):
    """
    Models a single Song that can be a part of zero or more Albums or
    Playlists, as well as followed by zero or more Users.
    """

    def __init__(self, name: str, artist):
        self.name = name
        self.artist = artist


class Album(Content):
    """
    Immutable collection of Songs made by the same Artist and grouped
    togther.

    * name       -- Name of the Album.   
    * arist      -- Name of the Artist that made the Album.   
    * songs      -- List of Songs in the Album.   
    """

    songs: list[Song]

    def __init__(self, name: str, artist, songs: list[Song]):
        self.name = name
        self.artist = artist
        self.songs = songs


class Playlist(Album):
    """
    Playlist class to be used in the interface between the back- and
    front-ends.

    * name       -- Name of the Playlist.   
    * arist      -- Name of the Artist that made the Playlist.   
    * songs      -- List of Songs in the Playlist.   
    * add_song() -- Adds a Song to the list of Songs.   
    """

    def __init__(self, name: str, songs: list[Song] = []):
        self.name = name
        self.songs = songs

    def add_song(self, song: Song):
        self.songs.append(song)
        lib.TODO("Playlist.add_song()")


class Artist:

    name: str
    albums: list[Album]
    songs: list[Song]

    def __init__(self,
                 name: str,
                 albums: list[Album] = [],
                 songs: list[Song] = []):
        self.name = name
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
    playlists: list[Playlist]
    favourites: Playlist
    followed_artists: list[Artist]
    followed_albums: list[Album]

    def __init__(self, handle):
        """
        Initialise a User instance with no playlists, no
        liked/favourited songs and no followed artists.
        """

        self.username = handle
        self.playlists = []
        self.favourites = Playlist("Favourites")
        self.followed_artists = []
        self.followed_albums = []

    def change_username(self, new_handle: str):
        lib.TODO("User.change_username()")
        self.username = new_handle

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
        playlist = Playlist(name)
        self.playlists.append(playlist)


if __name__ == "__main__":
    # Testing code:
    me = User("alchemistsGestalt")
    mono = Artist("Mono Inc.")
    heile_segen = Song("Heile, heile Segen", mono)
    teile = Song("Ich teile dich nicht", mono)
    nimmer = Album("Nimmermehr", mono, [heile_segen, teile])
    # These three calls to append (instead of having an Artist method deal
    # with them) should never happen, this is just here to set up the example.
    mono.songs.append(heile_segen)
    mono.songs.append(teile)
    mono.albums.append(nimmer)
    me.like_song(heile_segen)
    me.like_song(teile)
    me.follow_artist(mono)
    me.follow_album(nimmer)
    for song in me.favourites.songs:
        print(song.name)
    for artist in me.followed_artists:
        print(artist.name)
    for album in me.followed_albums:
        print(album.name)
