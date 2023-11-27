import sys
sys.path.append("./api_client")
import api_client

import requests
import json
import Youtube.models as yt_models

#Invokes a Search Request via api_client.
#Returns a SearchResponse object containing the results of the search request.
def search(request: yt_models.SearchRequest) -> yt_models.SearchResponse:
    #Creates the params string for the api_client.
    params = "?query=" + request.query + "&artCount=" + str(request.artist_count) + "&albCount=" + str(request.album_count) + "&sonCount=" + str(request.song_count)

    try:
        #gets the response (in json format) from the api_client.
        response = api_client.sendApiRequest(api_client.ApiControllers.Youtube.value, api_client.ApiRequests.Search.value, params)
    except requests.exceptions.ConnectionError:
        #If there is a connection error, return a SearchResponse with has_error set to True and error set to "Connection Error".
        return yt_models.SearchResponse(True, "Connection Error", [], [], [])

    try:
        #Parses the json response into a dictionary.
        parsed_data = json.loads(response)
    except json.decoder.JSONDecodeError:
        #If there is a JSON Decode Error, return a SearchResponse with has_error set to True and error set to "JSON Decode Error".
        return yt_models.SearchResponse(True, "JSON Decode Error", [], [], [])

    try:
        #Creates the SearchResponse object from the parsed data.
        songs = [yt_models.OnlineSong(song["id"], song["artistId"], song["name"], song["url"], song["coverArt"], song["duration"]) for song in parsed_data["songs"]]
        albums = [yt_models.OnlineAlbum(album["id"], album["artistId"], album["name"], album["coverArt"], []) for album in parsed_data["albums"]]
        artists = [yt_models.OnlineArtist(artist["id"], artist["name"], artist["coverArt"], [], []) for artist in parsed_data["artists"]]
        searchResponse = yt_models.SearchResponse(parsed_data["hasError"], parsed_data["error"], artists, albums, songs)
    except KeyError:
        #If there is a KeyError, return a SearchResponse with has_error set to True and error set to "Key Error".
        return yt_models.SearchResponse(True, "Key Error", [], [], [])

    #Return the SearchResponse object.
    return searchResponse

#Invokes a GetSongUrl Request via api_client.
#Returns a GetSongUrlRespose containing the url of the song.
def getSongUrl(song_id: str) -> yt_models.GetSongUrlResponse:
    #Creates the params string for the api_client.
    params = "?id=" + song_id

    try:
        #gets the response (in json format) from the api_client.
        response = api_client.sendApiRequest(api_client.ApiControllers.Youtube.value, api_client.ApiRequests.AudioUrl.value, params)
    except requests.exceptions.ConnectionError:
        #If there is a connection error, return a GetSongUrlResponse with has_error set to True and error set to "Connection Error".
        return yt_models.GetSongUrlResponse(True, "Connection Error", "")
    
    try:
        #Parses the json response into a dictionary.
        parsed_data = json.loads(response)
    except json.decoder.JSONDecodeError:
        #If there is a JSON Decode Error, return a GetSongUrlResponse with has_error set to True and error set to "JSON Decode Error".
        return yt_models.GetSongUrlResponse(True, "JSON Decode Error", "")
    
    try:
        #Creates the GetSongUrlResponse object from the parsed data.
        getSongUrlResponse = yt_models.GetSongUrlResponse(parsed_data["hasError"], parsed_data["error"], parsed_data["url"])
    except KeyError:
        #If there is a KeyError, return a GetSongUrlResponse with has_error set to True and error set to "Key Error".
        return yt_models.GetSongUrlResponse(True, "Key Error", "")
    
    #Return the GetSongUrlResponse object.
    return getSongUrlResponse

#Invokes a GetAlbumSongs Request via api_client.
#Returns a GetAlbumSongsResponse containing the songs of the album.
def getAlbumSongs(album_id: str) -> yt_models.GetAlbumSongsResponse:
    #Creates the params string for the api_client.
    params = "?id=" + album_id

    try:
        #gets the response (in json format) from the api_client.
        response = api_client.sendApiRequest(api_client.ApiControllers.Youtube.value, api_client.ApiRequests.AlbumSongs.value, params)
    except requests.exceptions.ConnectionError:
        #If there is a connection error, return a GetAlbumSongsResponse with has_error set to True and error set to "Connection Error".
        return yt_models.GetAlbumSongsResponse(True, "Connection Error", [])
    
    try:
        #Parses the json response into a dictionary.
        parsed_data = json.loads(response)
    except json.decoder.JSONDecodeError:
        #If there is a JSON Decode Error, return a GetAlbumSongsResponse with has_error set to True and error set to "JSON Decode Error".
        return yt_models.GetAlbumSongsResponse(True, "JSON Decode Error", [])
    
    try:
        #Creates the GetAlbumSongsResponse object from the parsed data.
        songs = [yt_models.OnlineSong(song["id"], song["artistId"], song["name"], song["url"], song["coverArt"], song["duration"]) for song in parsed_data["albumSongs"]]
        getAlbumSongsResponse = yt_models.GetAlbumSongsResponse(parsed_data["hasError"], parsed_data["error"], songs)
    except KeyError:
        #If there is a KeyError, return a GetAlbumSongsResponse with has_error set to True and error set to "Key Error".
        return yt_models.GetAlbumSongsResponse(True, "Key Error", [])
    
    #Return the GetAlbumSongsResponse object.
    return getAlbumSongsResponse

#Invokes a GetArtistAlbums Request via api_client.
#Returns a GetArtistAlbumsResponse containing the albums of the artist.
def getArtistAlbums(artist_id: str) -> yt_models.GetArtistAlbumsResponse:
    #Creates the params string for the api_client.
    params = "?id=" + artist_id

    try:
        #gets the response (in json format) from the api_client.
        response = api_client.sendApiRequest(api_client.ApiControllers.Youtube.value, api_client.ApiRequests.ArtistAlbums.value, params)
    except requests.exceptions.ConnectionError:
        #If there is a connection error, return a GetArtistAlbumsResponse with has_error set to True and error set to "Connection Error".
        return yt_models.GetArtistAlbumsResponse(True, "Connection Error", [])
    
    try:
        #Parses the json response into a dictionary.
        parsed_data = json.loads(response)
    except json.decoder.JSONDecodeError:
        #If there is a JSON Decode Error, return a GetArtistAlbumsResponse with has_error set to True and error set to "JSON Decode Error".
        return yt_models.GetArtistAlbumsResponse(True, "JSON Decode Error", [])
    
    try:
        #Creates the GetArtistAlbumsResponse object from the parsed data.
        albums = [yt_models.OnlineAlbum(album["id"], album["artistId"], album["name"], album["coverArt"], []) for album in parsed_data["artistAlbums"]]
        getArtistAlbumsResponse = yt_models.GetArtistAlbumsResponse(parsed_data["hasError"], parsed_data["error"], albums)
    except KeyError:
        #If there is a KeyError, return a GetArtistAlbumsResponse with has_error set to True and error set to "Key Error".
        return yt_models.GetArtistAlbumsResponse(True, "Key Error", [])
    
    #Return the GetArtistAlbumsResponse object.
    return getArtistAlbumsResponse

#Invokes a GetArtistSongs Request via api_client.
#Returns a GetArtistSongsResponse containing the songs of the artist.
def getArtistSongs(artist_id: str) -> yt_models.GetArtistSongsResponse:
    #Creates the params string for the api_client.
    params = "?id=" + artist_id

    try:
        #gets the response (in json format) from the api_client.
        response = api_client.sendApiRequest(api_client.ApiControllers.Youtube.value, api_client.ApiRequests.ArtistSongs.value, params)
    except requests.exceptions.ConnectionError:
        #If there is a connection error, return a GetArtistSongsResponse with has_error set to True and error set to "Connection Error".
        return yt_models.GetArtistSongsResponse(True, "Connection Error", [])
    
    try:
        #Parses the json response into a dictionary.
        parsed_data = json.loads(response)
    except json.decoder.JSONDecodeError:
        #If there is a JSON Decode Error, return a GetArtistSongsResponse with has_error set to True and error set to "JSON Decode Error".
        return yt_models.GetArtistSongsResponse(True, "JSON Decode Error", [])
    
    try:
        #Creates the GetArtistSongsResponse object from the parsed data.
        songs = [yt_models.OnlineSong(song["id"], song["artistId"], song["name"], song["url"], song["coverArt"], song["duration"]) for song in parsed_data["songs"]]
        getArtistSongsResponse = yt_models.GetArtistSongsResponse(parsed_data["hasError"], parsed_data["error"], songs)
    except KeyError:
        #If there is a KeyError, return a GetArtistSongsResponse with has_error set to True and error set to "Key Error".
        return yt_models.GetArtistSongsResponse(True, "Key Error", [])
    
    #Return the GetArtistSongsResponse object.
    return getArtistSongsResponse

if __name__ == "__main__":
    request = yt_models.SearchRequest("eminem", 5, 5, 5)
    search_results = search(request)
    print(search_results.artists)
    print(search_results.albums)
    print(search_results.songs)
    print(search_results.has_error)
    print(search_results.error)
