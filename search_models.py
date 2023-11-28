"""
Classes for data sent to and from the C# back-end.
"""

from data_models import *
import lib

class SearchResults():
    """
    Class to model data sent back by the C# back-end.
    """

    artists: list[Artist]
    albums : list[Album ]
    songs  : list[Song  ]

    def __init__(self,
                 artists: list[Artist],
                 albums: list[Album],
                 songs: list[Song]):
        self.artists = artists
        self.albums  = albums
        self.songs   = songs


class SearchRequest():
    """
    Class modelling data to be sent to the C# back-end.
    """

    query       : str
    artist_count: int
    album_count : int
    song_count  : int

    def __init__(self, query, artist_count, album_count, song_count):
        self.query        = query
        self.artist_count = artist_count
        self.album_count  = album_count
        self.song_count   = song_count
