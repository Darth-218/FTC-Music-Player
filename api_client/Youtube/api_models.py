import sys
sys.path.append("../FTC-Music-Player")

from datetime import timedelta
import data_models

#Represents a Song object that is obtained from the API.
class OnlineSong(data_models.Song):
    id: str
    artist_id: str

    def __init__(self, id: str, artist_id: str, name: str, url: str, cover_art: str, duration: timedelta):
        self.id = id
        self.artist_id = artist_id
        self.name = name
        self._url = url
        self.cover_art = cover_art
        self.duration = duration
        self.artist = 'artist'
        self._path = ''

#Represents an Album object that is obtained from the API.
class OnlineAlbum(data_models.Album):
    id: str
    artist_id: str
    cover_art: str

    def __init__(self, id: str, artist_id: str, name: str, cover_art: str, songs: list[OnlineSong]):
        self.id = id
        self.artist_id = artist_id
        self.name = name
        self.cover_art = cover_art
        self.artist = "artist"
        self.songs = songs
        self._path = ''

#Represents an Artist object that is obtained from the API.
class OnlineArtist(data_models.Artist):
    id: str
    cover_art: str

    def __init__(self, id: str, name: str, cover_art: str, albums: list[OnlineAlbum], songs: list[OnlineSong]):
        self.id = id
        self.name = name
        self.cover_art = cover_art
        self.albums = albums
        self.songs = songs
        self._path = ''
        self._url = ''

#Represents a search request to the API.
class SearchRequest():
    query: str
    artist_count: int
    album_count: int
    song_count: int

    def __init__(self, query, artist_count, album_count, song_count):
        self.query        = query
        self.artist_count = artist_count
        self.album_count  = album_count
        self.song_count   = song_count


#Represents the search response from the API.
class SearchResponse:
    has_error: bool
    error: str
    artists: list[OnlineArtist]
    albums: list[OnlineAlbum]
    songs: list[OnlineSong]

    def __init__(self, has_error: bool, error: str, artists: list[OnlineArtist], albums: list[OnlineAlbum], songs: list[OnlineSong]):
        self.id = id
        self.has_error = has_error
        self.error = error
        self.artists = artists
        self.albums = albums
        self.songs = songs

#Represents a GetSongUrl response from the API.
class GetSongUrlResponse:
    has_error: bool
    error: str
    url: str

    def __init__(self, has_error: bool, error: str, url: str):
        self.has_error = has_error
        self.error = error
        self.url = url

#Represents a GetAlbumSongs response from the API.
class GetAlbumSongsResponse:
    has_error: bool
    error: str
    songs: list[OnlineSong]

    def __init__(self, has_error: bool, error: str, songs: list[OnlineSong]):
        self.has_error = has_error
        self.error = error
        self.songs = songs

#Represents a GetArtistAlbums response from the API.
class GetArtistAlbumsResponse:
    has_error: bool
    error: str
    albums: list[OnlineAlbum]

    def __init__(self, has_error: bool, error: str, albums: list[OnlineAlbum]):
        self.has_error = has_error
        self.error = error
        self.albums = albums

#Represents a GetArtistSongs response from the API.
class GetArtistSongsResponse:
    has_error: bool
    error: str
    songs: list[OnlineSong]

    def __init__(self, has_error: bool, error: str, songs: list[OnlineSong]):
        self.has_error = has_error
        self.error = error
        self.songs = songs

#Represents a GetSuggestions Request to the API.
class GetSuggestionsRequest:
    artist_count: int
    album_count: int
    song_count: int
    interests: str

    def __init__(self, artist_count, album_count, song_count, interests):
        self.artist_count = artist_count
        self.album_count  = album_count
        self.song_count   = song_count
        self.interests    = interests

#Represents a GetSuggestions response from the API.
class GetSuggestionsResponse:
    has_error: bool
    error: str
    artists: list[OnlineArtist]
    albums: list[OnlineAlbum]
    songs: list[OnlineSong]

    def __init__(self, has_error: bool, error: str, artists: list[OnlineArtist], albums: list[OnlineAlbum], songs: list[OnlineSong]):
        self.has_error = has_error
        self.error = error
        self.artists = artists
        self.albums = albums
        self.songs = songs

#Represents a GetArtistLatestRelease response from the API.
class GetArtistLatestReleaseResponse:
    has_error: bool
    error: str
    latestRelease: list[OnlineSong]

    def __init__(self, has_error: bool, error: str, latestRelease: list[OnlineSong]):
        self.has_error = has_error
        self.error = error
        self.latestRelease = latestRelease