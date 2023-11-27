"""
api_client doc str
"""


from enum import Enum
import requests

#Server IP Address
serverIp = "10.2.157.102:5239" #Please update this to the IP Address of the server.

#API Controller Options
class ApiControllers(Enum):
    Youtube = "/Youtube"

#API Request Options
class ApiRequests(Enum):
    Search       = "/Search"
    AudioUrl     = "/GetAudioUrl"
    AlbumSongs   = "/GetAlbumSongs"
    ArtistAlbums = "/GetArtistAlbums"
    ArtistSongs  = "/GetArtistSongs"
    

#Sends a request to the server and returns the response (is json format).
#Takes in the controller, request, and params as strings.
def sendApiRequest(controller: str, request: str, params: str) -> str:
    response = requests.get("http://" + serverIp + controller + request + params)
    # print(response.text)
    return response.text
