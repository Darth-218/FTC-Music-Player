"""
This file builds the requests to the API server via the api_client and parses the responses into the models defined in models.py.
"""


import sys
sys.path.append("../api_client/Youtube/")

import api_client.api_client as api_client
import requests
import json
import api_client.Youtube.api_models as yt_models
import lib
from datetime import timedelta


def search(request: yt_models.SearchRequest) -> yt_models.SearchResponse:
    """
    Invokes a Search Request via api_client.
    
    Takes in a SearchRequest object.
    
    Returns a SearchResponse object containing the results of the search request.
    """
    
    lib.logger("api_client/Youtube/youtube/search", "Searching for: " + request.query + " with artist_count: " + str(request.artist_count) + " album_count: " + str(request.album_count) + " song_count: " + str(request.song_count) + ".")

    #Creates the params string for the api_client.
    params = "?query=" + request.query + "&artCount=" + str(request.artist_count) + "&albCount=" + str(request.album_count) + "&sonCount=" + str(request.song_count)

    try:
        #gets the response (in json format) from the api_client.
        response = api_client.sendApiRequest(api_client.ApiControllers.Youtube.value, api_client.ApiRequests.Search.value, params)
    except requests.exceptions.ConnectionError:
        #If there is a connection error, return a SearchResponse with has_error set to True and error set to "Connection Error".
        lib.logger("api_client/Youtube/youtube/search", "Connection Error.")
        return yt_models.SearchResponse(True, "Connection Error", [], [], [])

    try:
        #Parses the json response into a dictionary.
        parsed_data = json.loads(response)
    except json.decoder.JSONDecodeError:
        #If there is a JSON Decode Error, return a SearchResponse with has_error set to True and error set to "JSON Decode Error".
        lib.logger("api_client/Youtube/youtube/search", "JSON Decode Error.")
        return yt_models.SearchResponse(True, "JSON Decode Error", [], [], [])

    try:
        #Creates the SearchResponse object from the parsed data.
        songs = [yt_models.OnlineSong(song["id"], song["artistId"], song["name"], song["url"], song["coverArt"], lib.str_to_delta(song['duration'])) for song in parsed_data["songs"]]
        albums = [yt_models.OnlineAlbum(album["id"], album["artistId"], album["name"], album["coverArt"], []) for album in parsed_data["albums"]]
        artists = [yt_models.OnlineArtist(artist["id"], artist["name"], artist["coverArt"], [], []) for artist in parsed_data["artists"]]
        searchResponse = yt_models.SearchResponse(parsed_data["hasError"], parsed_data["error"], artists, albums, songs)
    except KeyError:
        #If there is a KeyError, return a SearchResponse with has_error set to True and error set to "Key Error".
        lib.logger("api_client/Youtube/youtube/search", "Key Error.")
        return yt_models.SearchResponse(True, "Key Error", [], [], [])

    #Return the SearchResponse object.
    return searchResponse


def getSongUrl(song_id: str) -> yt_models.GetSongUrlResponse:
    """
    Invokes a GetSongUrl Request via api_client.
    
    Takes in a song_id as a string.
    
    Returns a GetSongUrlRespose containing the url of the song.
    """

    lib.logger("api_client/Youtube/youtube/getSongUrl", "Getting song url for song_id: " + song_id + ".")
    
    #Creates the params string for the api_client.
    params = "?id=" + song_id

    try:
        #gets the response (in json format) from the api_client.
        response = api_client.sendApiRequest(api_client.ApiControllers.Youtube.value, api_client.ApiRequests.AudioUrl.value, params)
    except requests.exceptions.ConnectionError:
        #If there is a connection error, return a GetSongUrlResponse with has_error set to True and error set to "Connection Error".
        lib.logger("api_client/Youtube/youtube/getSongUrl", "Connection Error.")
        return yt_models.GetSongUrlResponse(True, "Connection Error", "")
    
    try:
        #Parses the json response into a dictionary.
        parsed_data = json.loads(response)
    except json.decoder.JSONDecodeError:
        #If there is a JSON Decode Error, return a GetSongUrlResponse with has_error set to True and error set to "JSON Decode Error".
        lib.logger("api_client/Youtube/youtube/getSongUrl", "JSON Decode Error.")
        return yt_models.GetSongUrlResponse(True, "JSON Decode Error", "")
    
    try:
        #Creates the GetSongUrlResponse object from the parsed data.
        getSongUrlResponse = yt_models.GetSongUrlResponse(parsed_data["hasError"], parsed_data["error"], parsed_data["url"])
    except KeyError:
        #If there is a KeyError, return a GetSongUrlResponse with has_error set to True and error set to "Key Error".
        lib.logger("api_client/Youtube/youtube/getSongUrl", "Key Error.")
        return yt_models.GetSongUrlResponse(True, "Key Error", "")
    
    #Return the GetSongUrlResponse object.
    return getSongUrlResponse


def getAlbumSongs(album_id: str) -> yt_models.GetAlbumSongsResponse:
    """
    Invokes a GetAlbumSongs Request via api_client.
    
    Takes in a album_id as a string.
    
    Returns a GetAlbumSongsResponse containing the songs of the album.
    """

    lib.logger("api_client/Youtube/youtube/getAlbumSongs", "Getting album songs for album_id: " + album_id + ".")
    
    #Creates the params string for the api_client.
    params = "?id=" + album_id

    try:
        #gets the response (in json format) from the api_client.
        response = api_client.sendApiRequest(api_client.ApiControllers.Youtube.value, api_client.ApiRequests.AlbumSongs.value, params)
    except requests.exceptions.ConnectionError:
        #If there is a connection error, return a GetAlbumSongsResponse with has_error set to True and error set to "Connection Error".
        lib.logger("api_client/Youtube/youtube/getAlbumSongs", "Connection Error.")
        return yt_models.GetAlbumSongsResponse(True, "Connection Error", [])
    
    try:
        #Parses the json response into a dictionary.
        parsed_data = json.loads(response)
    except json.decoder.JSONDecodeError:
        #If there is a JSON Decode Error, return a GetAlbumSongsResponse with has_error set to True and error set to "JSON Decode Error".
        lib.logger("api_client/Youtube/youtube/getAlbumSongs", "JSON Decode Error.")
        return yt_models.GetAlbumSongsResponse(True, "JSON Decode Error", [])
    
    try:
        #Creates the GetAlbumSongsResponse object from the parsed data.
        songs = [yt_models.OnlineSong(song["id"], song["artistId"], song["name"], song["url"], song["coverArt"], lib.str_to_delta(song['duration'])) for song in parsed_data["albumSongs"]]
        getAlbumSongsResponse = yt_models.GetAlbumSongsResponse(parsed_data["hasError"], parsed_data["error"], songs)
    except KeyError:
        #If there is a KeyError, return a GetAlbumSongsResponse with has_error set to True and error set to "Key Error".
        lib.logger("api_client/Youtube/youtube/getAlbumSongs", "Key Error.")
        return yt_models.GetAlbumSongsResponse(True, "Key Error", [])
    
    #Return the GetAlbumSongsResponse object.
    return getAlbumSongsResponse


def getArtistAlbums(artist_id: str) -> yt_models.GetArtistAlbumsResponse:
    """
    Invokes a GetArtistAlbums Request via api_client.
    
    Takes in a artist_id as a string.
    
    Returns a GetArtistAlbumsResponse containing the albums of the artist.
    """

    lib.logger("api_client/Youtube/youtube/getArtistAlbums", "Getting artist albums for artist_id: " + artist_id + ".")
    
    #Creates the params string for the api_client.
    params = "?id=" + artist_id

    try:
        #gets the response (in json format) from the api_client.
        response = api_client.sendApiRequest(api_client.ApiControllers.Youtube.value, api_client.ApiRequests.ArtistAlbums.value, params)
    except requests.exceptions.ConnectionError:
        #If there is a connection error, return a GetArtistAlbumsResponse with has_error set to True and error set to "Connection Error".
        lib.logger("api_client/Youtube/youtube/getArtistAlbums", "Connection Error.")
        return yt_models.GetArtistAlbumsResponse(True, "Connection Error", [])
    
    try:
        #Parses the json response into a dictionary.
        parsed_data = json.loads(response)
    except json.decoder.JSONDecodeError:
        #If there is a JSON Decode Error, return a GetArtistAlbumsResponse with has_error set to True and error set to "JSON Decode Error".
        lib.logger("api_client/Youtube/youtube/getArtistAlbums", "JSON Decode Error.")
        return yt_models.GetArtistAlbumsResponse(True, "JSON Decode Error", [])
    
    try:
        #Creates the GetArtistAlbumsResponse object from the parsed data.
        albums = [yt_models.OnlineAlbum(album["id"], album["artistId"], album["name"], album["coverArt"], []) for album in parsed_data["artistAlbums"]]
        getArtistAlbumsResponse = yt_models.GetArtistAlbumsResponse(parsed_data["hasError"], parsed_data["error"], albums)
    except KeyError:
        #If there is a KeyError, return a GetArtistAlbumsResponse with has_error set to True and error set to "Key Error".
        lib.logger("api_client/Youtube/youtube/getArtistAlbums", "Key Error.")
        return yt_models.GetArtistAlbumsResponse(True, "Key Error", [])
    
    #Return the GetArtistAlbumsResponse object.
    return getArtistAlbumsResponse


def getArtistSongs(artist_id: str) -> yt_models.GetArtistSongsResponse:
    """
    Invokes a GetArtistSongs Request via api_client.
    
    Takes in a artist_id as a string.
    
    Returns a GetArtistSongsResponse containing the songs of the artist.
    """

    lib.logger("api_client/Youtube/youtube/getArtistSongs", "Getting artist songs for artist_id: " + artist_id + ".")
    
    #Creates the params string for the api_client.
    params = "?id=" + artist_id

    try:
        #gets the response (in json format) from the api_client.
        response = api_client.sendApiRequest(api_client.ApiControllers.Youtube.value, api_client.ApiRequests.ArtistSongs.value, params)
    except requests.exceptions.ConnectionError:
        #If there is a connection error, return a GetArtistSongsResponse with has_error set to True and error set to "Connection Error".
        lib.logger("api_client/Youtube/youtube/getArtistSongs", "Connection Error.")
        return yt_models.GetArtistSongsResponse(True, "Connection Error", [])
    
    try:
        #Parses the json response into a dictionary.
        parsed_data = json.loads(response)
    except json.decoder.JSONDecodeError:
        #If there is a JSON Decode Error, return a GetArtistSongsResponse with has_error set to True and error set to "JSON Decode Error".
        lib.logger("api_client/Youtube/youtube/getArtistSongs", "JSON Decode Error.")
        return yt_models.GetArtistSongsResponse(True, "JSON Decode Error", [])
    
    try:
        #Creates the GetArtistSongsResponse object from the parsed data.
        songs = [yt_models.OnlineSong(song["id"], song["artistId"], song["name"], song["url"], song["coverArt"], lib.str_to_delta(song['duration'])) for song in parsed_data["songs"]]
        getArtistSongsResponse = yt_models.GetArtistSongsResponse(parsed_data["hasError"], parsed_data["error"], songs)
    except KeyError:
        #If there is a KeyError, return a GetArtistSongsResponse with has_error set to True and error set to "Key Error".
        lib.logger("api_client/Youtube/youtube/getArtistSongs", "Key Error.")
        return yt_models.GetArtistSongsResponse(True, "Key Error", [])
    
    #Return the GetArtistSongsResponse object.
    return getArtistSongsResponse

def getSuggestions(request: yt_models.GetSuggestionsRequest) -> yt_models.GetSuggestionsResponse:
    """
    Invokes a GetSuggestions Request via api_client.
    
    Takes in a GetSuggestionsRequest object.
    
    Returns a GetSuggestionsResponse containing the suggestions.
    """
    
    lib.logger("api_client/Youtube/youtube/getSuggestions", "Getting suggestions for interests: " + request.interests + " with artist_count: " + str(request.artist_count) + " album_count: " + str(request.album_count) + " song_count: " + str(request.song_count) + ".")

    #Creates the params string for the api_client.
    params = "?artCount=" + str(request.artist_count) + "&albCount=" + str(request.album_count) + "&sonCount=" + str(request.song_count) + "&interests=" + request.interests

    try:
        #gets the response (in json format) from the api_client.
        response = api_client.sendApiRequest(api_client.ApiControllers.Youtube.value, api_client.ApiRequests.Suggestions.value, params)
    except requests.exceptions.ConnectionError:
        #If there is a connection error, return a GetSuggestionsResponse with has_error set to True and error set to "Connection Error".
        lib.logger("api_client/Youtube/youtube/getSuggestions", "Connection Error.")
        return yt_models.GetSuggestionsResponse(True, "Connection Error", [], [], [])
    
    try:
        #Parses the json response into a dictionary.
        parsed_data = json.loads(response)
    except json.decoder.JSONDecodeError:
        #If there is a JSON Decode Error, return a GetSuggestionsResponse with has_error set to True and error set to "JSON Decode Error".
        lib.logger("api_client/Youtube/youtube/getSuggestions", "JSON Decode Error.")
        return yt_models.GetSuggestionsResponse(True, "JSON Decode Error", [], [], [])
    
    try:
        #Creates the GetSuggestionsResponse object from the parsed data.
        songs = [yt_models.OnlineSong(song["id"], song["artistId"], song["name"], song["url"], song["coverArt"], lib.str_to_delta(song['duration'])) for song in parsed_data["songs"]]
        albums = [yt_models.OnlineAlbum(album["id"], album["artistId"], album["name"], album["coverArt"], []) for album in parsed_data["albums"]]
        artists = [yt_models.OnlineArtist(artist["id"], artist["name"], artist["coverArt"], [], []) for artist in parsed_data["artists"]]
        getSuggestionsResponse = yt_models.GetSuggestionsResponse(parsed_data["hasError"], parsed_data["error"], artists, albums, songs)
    except KeyError:
        #If there is a KeyError, return a GetSuggestionsResponse with has_error set to True and error set to "Key Error".
        lib.logger("api_client/Youtube/youtube/getSuggestions", "Key Error.")
        return yt_models.GetSuggestionsResponse(True, "Key Error", [], [], [])

    #Return the GetSuggestionsResponse object.
    return getSuggestionsResponse

def getLatestRelease(artistId: str):
    """
    Invokes a GetArtistLatestRelease Request via api_client.
    
    Takes in a channelId as a string.
    
    Returns a GetArtistLatestReleaseResponse containing the latest release of the artist.
    """

    lib.logger("api_client/Youtube/youtube/getArtistLatestRelease", "Getting latest release for artistId: " + artistId + ".")
    
    #Creates the params string for the api_client.
    params = "?artistId=" + artistId

    try:
        #gets the response (in json format) from the api_client.
        response = api_client.sendApiRequest(api_client.ApiControllers.Youtube.value, api_client.ApiRequests.ArtistLatestRelease.value, params)
    except requests.exceptions.ConnectionError:
        #If there is a connection error, return a GetArtistLatestReleaseResponse with has_error set to True and error set to "Connection Error".
        lib.logger("api_client/Youtube/youtube/getArtistLatestRelease", "Connection Error.")
        return yt_models.GetArtistLatestReleaseResponse(True, "Connection Error", "")
    
    try:
        #Parses the json response into a dictionary.
        parsed_data = json.loads(response)
    except json.decoder.JSONDecodeError:
        #If there is a JSON Decode Error, return a GetArtistLatestReleaseResponse with has_error set to True and error set to "JSON Decode Error".
        lib.logger("api_client/Youtube/youtube/getArtistLatestRelease", "JSON Decode Error.")
        return yt_models.GetArtistLatestReleaseResponse(True, "JSON Decode Error", "")
    
    try:
        #Creates the GetArtistLatestReleaseResponse object from the parsed data.
        latestRelease  = [yt_models.OnlineSong(song["id"], song["artistId"], song["name"], song["url"], song["coverArt"], lib.str_to_delta(song['duration'])) for song in parsed_data["latestRelease"]]
        getArtistLatestReleaseResponse = yt_models.GetArtistLatestReleaseResponse(parsed_data["hasError"], parsed_data["error"], latestRelease)
    except KeyError:
        #If there is a KeyError, return a GetArtistLatestReleaseResponse with has_error set to True and error set to "Key Error".
        lib.logger("api_client/Youtube/youtube/getArtistLatestRelease", "Key Error.")
        return yt_models.GetArtistLatestReleaseResponse(True, "Key Error", "")
    
    #Return the GetArtistLatestReleaseResponse object.
    return getArtistLatestReleaseResponse

if __name__ == "__main__":
    res = getLatestRelease('UClQPk2WbC23z3eogxPbbOjw')
    print(res.has_error)
    print(res.error)
    print(res.latestRelease[0].name)
