"""
Playlist
"""

from song import Song

class Playlist():
    """
    list of plays
    """

    songs: [Song]

    def __init__(self):
        self.songs = []
