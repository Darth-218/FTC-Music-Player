#!/usr/bin/env /usr/bin/python3
import sys
sys.path.append("./")
import youtube
import api_models

# Example usage of the Youtube API.

if __name__ == "__main__":
  #Get the search query from the user.
  query = input("Enter the search query: ")

  #Create a SearchRequest object.
  request = api_models.SearchRequest(query, 5, 5, 10) #The numbers represent the number of artists, albums, and songs to return respectively.

  # *Get the search results from the API.*
  search_response = youtube.search(request) #This returns a SearchResponse object.
  if not search_response.has_error: #Check if there is no error.
    #Print the search results.
    print("Artists:")
    for artist in search_response.artists:
      print(artist.name)

    print("\nAlbums:")
    for album in search_response.albums:
      print(album.name)

    print("\nSongs:")
    for song in search_response.songs:
      print(song.name)

    # *Get the direct url of the first song.*
    audio_response = youtube.getSongUrl(search_response.songs[0].id) #This returns a GetAudioUrlResponse object.

    if not audio_response.has_error: #Check if there is no error.
      #Print the direct url of the song.
      print("\nDirect Url: " + audio_response.url)
    else: #If there is an error, print the error.         
      print("\nError: " + audio_response.error)

    # *Get the albums of the first artist.*
    artist_albums_response = youtube.getArtistAlbums(search_response.artists[0].id)

    if not artist_albums_response.has_error: #Check if there is no error.
      #Print the albums of the artist.
      print("\nAlbums of the first Artist:")
      for album in artist_albums_response.albums:
        print(album.name)
    else: #If there is an error, print the error.
      print("\nError: " + artist_albums_response.error)

    # *Get the songs of the first album.*
    album_songs_response = youtube.getAlbumSongs(search_response.albums[0].id)

    if not album_songs_response.has_error: #Check if there is no error.
      #Print the songs of the album.
      print("\nSongs of the first Album:")
      for song in album_songs_response.songs:
        print(song.name)
    else: #If there is an error, print the error.
      print("\nError: " + album_songs_response.error)

    # *Get the songs of the first artist.*
    artist_songs_response = youtube.getArtistSongs(search_response.artists[0].id)

    if not artist_songs_response.has_error: #Check if there is no error.
      #Print the songs of the artist.
      print("\nSongs of the first Artist:")
      for song in artist_songs_response.songs:
        print(song.name)
    else: #If there is an error, print the error.
      print("\nError: " + artist_songs_response.error)
  else: #If there is an error, print the error.
    print("Error: " + search_response.error)
