from enum import Enum
import requests

serverIp = "10.2.157.102:5239"

class ApiControllers(Enum):
    Youtube = "/Youtube"

class ApiRequests(Enum):
    Search = "/Search"
    AudioUrl = "/GetAudioUrl"
    AlbumSongs = "/GetAlbumSongs"
    ArtistAlbums = "/GetArtistAlbums"
    ArtistSongs = "/GetArtistSongs"
    


def sendApiRequest( controller: ApiControllers, request: ApiRequests) -> str:
    response = requests.get("http://" + serverIp + controller + request)
    return response.text