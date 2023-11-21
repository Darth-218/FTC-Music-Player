"""
Defines a User class to contain data such as:
    * username
    * list of playlists
    * liked/favourited songs
    * list of followed artists
"""

from playlist import Playlist
from artist import Artist

class User():
    """
    A User class to model the data for a user of the application.
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
        self.loved     = Playlist()


if __name__ == "__main__":
    me = User("alchemistsGestalt")
    print(me.username)
