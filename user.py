"""
Defines a User class to contain data such as:   

    * username   
    * list of playlists   
    * liked/favourited songs   
    * list of followed artists   
"""

from playlist import Playlist
from artist   import Artist
from song     import Song
import lib

class User():
    """
    A User class to model the data for a user of the application.

    ```
    username  -- Personal identifier   
    playlists -- List of playlists/albums the user has saved   
    loved     -- Special playlist of the user’s favourite songs.   
    followed  -- List of all the artists that the user has followed.   
    ```
    """

    username : str
    playlists: list[Playlist]
    loved    : Playlist
    followed : list[Artist]

    def __init__(self, handle):
        """
        Initialise a User instance with no playlists, no
        liked/favourited songs and no followed artists.
        """

        self.username  = handle
        self.playlists = []
        self.loved     = Playlist("Liked Songs")

    def change_username(self, new_handle: str):
        lib.TODO("Interact with the API to change a user’s username.")
        self.username = new_handle


    def like_song(self, song: Song):
        lib.TODO(
            "Interact with the API to add a song to the user’s liked songs."
        )

        self.loved.add_song(song)


    def follow_artist(self, artist: Artist):
        lib.TODO("follow_artist")
        self.followed.append(artist)


    def create_playlist(self, name: str):
        playlist = Playlist(name)
        self.playlists.append(playlist)


if __name__ == "__main__":
    me = User("alchemistsGestalt")
    print(me.username)
