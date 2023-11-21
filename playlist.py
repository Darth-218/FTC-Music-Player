"""
Defines a Playlist class.
"""

from song import Song
import lib

class Playlist():
    """
    Playlist class to be used in the interface between the back- and
    front-ends.

    songs    -- List of songs in the playlist.
    add_song -- Adds a song to the list of songs.
    """

    name : str
    songs: list[Song]

    def __init__(self, name: str):
        self.name  = name
        self.songs = []


    def add_song(self, song: Song):
        self.songs.append(song)
        lib.TODO("Do some more logic here.")
