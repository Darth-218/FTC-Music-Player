"""
MODEhalrd
"""

from data_models import *

class SearchResults():
    """
    SearchResults
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
    SearchRequst
    """

    query: str
    artist_count: int
    album_count: int
    song_count: int

    def __init__(self, query, artist_count, album_count, song_count):
        self.query        = query
        self.artist_count = artist_count
        self.album_count  = album_count
        self.song_count   = song_count
