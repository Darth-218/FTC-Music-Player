using FTC_MusicPlayerAPI.Models;
using System.Diagnostics.Metrics;
using YoutubeExplode;
using YoutubeExplode.Common;
using System.Text.RegularExpressions;
using YoutubeExplode.Playlists;
using System.Diagnostics;

namespace FTC_MusicPlayerAPI.Services
{
    public class YoutubeExplodeService : IYoutubeService
    {
        private YoutubeClient Client { get; set; } = new YoutubeClient();
        public async Task<SearchResponse> Search(SearchRequest request)
        {
            SearchResponse response = new SearchResponse()
            {
                Artists = new List<Artist>(),
                Albums = new List<Album>(),
                Songs = new List<Song>()
            };

            try
            {
                Task artistsTask = Task.Run(async () =>
                {
                    int counter = 0;
                    var rawArtists = Client.Search.GetChannelsAsync(request.Query);

                    await foreach (var rawArtist in rawArtists)
                    {
                        var cha = await Client.Channels.GetAsync(rawArtist.Id);

                        if (counter == request.ArtistsCount)
                        {
                            break;
                        }
                        counter++;
                        response.Artists.Add(new Artist()
                        {
                            Id = rawArtist.Id.ToString(),
                            Name = rawArtist.Title,
                            CoverArt = rawArtist.Thumbnails.GetWithHighestResolution().Url,
                        });
                    }
                });

                Task albumsTask = Task.Run(async () =>
                {
                    int counter = 0;
                    var rawAlbums = Client.Search.GetPlaylistsAsync(request.Query);

                    await foreach (var rawAlbum in rawAlbums)
                    {
                        if (counter == request.AlbumsCount)
                        {
                            break;
                        }
                        counter++;
                        response.Albums.Add(new Album()
                        {
                            Id = rawAlbum.Id.ToString(),
                            ArtistId = rawAlbum.Author == null ? null : rawAlbum.Author!.ChannelId.ToString(),
                            Name = rawAlbum.Title,
                            CoverArt = rawAlbum.Thumbnails.GetWithHighestResolution().Url,
                        });
                    }
                });


                Task songsTask = Task.Run(async () =>
                {
                    int counter = 0;
                    var rawSongs = Client.Search.GetVideosAsync(request.Query);
                    await foreach (var rawSong in rawSongs)
                    {
                        if (counter == request.SongsCount)
                        {
                            break;
                        }
                        counter++;
                        response.Songs.Add(new Song()
                        {
                            Id = rawSong.Id.ToString(),
                            ArtistId = rawSong.Author == null ? null : rawSong.Author!.ChannelId.ToString(),
                            Name = rawSong.Title,
                            CoverArt = rawSong.Thumbnails.GetWithHighestResolution().Url,
                            Duration = rawSong.Duration,
                            Url = rawSong.Url
                        });
                    }
                });

                await Task.WhenAll(artistsTask, albumsTask, songsTask);
                return response;
            }
            catch (Exception)
            {
                throw;
            }
        }

        public async Task<AudioUrlResponse> GetSongUrl(string songId)
        {
            try
            {
                var video = await Client.Videos.GetAsync(songId);
                var streamsManifest = await Client.Videos.Streams.GetManifestAsync(video.Id);

                var audioStreams = streamsManifest.GetAudioOnlyStreams();
                var bestAudioStream = audioStreams.FirstOrDefault();

                AudioUrlResponse response = new() { HasError = false, Error = "", Url = bestAudioStream!.Url };

                return response;
            }
            catch (Exception)
            {
                throw;
            }
        }

        public async Task<AlbumSongsResponse> GetAlbumSongs(string albumId)
        {
            try
            {
                var contents = Client.Playlists.GetVideosAsync(albumId);
                List<Song> songs = new List<Song>();

                await foreach (var song in contents)
                {
                    songs.Add(new()
                    {
                        Id = song.Id,
                        ArtistId = song.Author.ChannelId.ToString(),
                        Name = song.Title,
                        CoverArt = song.Thumbnails.GetWithHighestResolution().Url,
                        Duration = song.Duration,
                        Url = song.Url,
                    });
                }

                AlbumSongsResponse response = new() { AlbumSongs = songs, Error = "", HasError = false };
                return response;
            }
            catch (Exception)
            {
                throw;
            }
        }

        public async Task<ArtistAlbumsResponse> GetArtistAlbums(string artistId)
        {
            List<Album> albums = new();
            Console.WriteLine("Getting Playlists...");
            List<string> ids;
            try
            {
                HttpClient client = new();
                HttpResponseMessage response = await client.GetAsync($"https://www.youtube.com/channel/{artistId}/playlists");
                string responseBody = await response.Content.ReadAsStringAsync();

                ids = GetChannelPlaylistsIds(artistId.ToString(), responseBody);

                Console.WriteLine($"ids.length = {ids.Count}");

                PlaylistClient playlistClient = new(new HttpClient());

                for (int i = 0; i < ids.Count; i++)
                {
                    var playlist = await playlistClient.GetAsync(ids[i]);
                    Album album = new()
                    {
                        Id = playlist.Id.ToString(),
                        ArtistId = playlist.Author!.ChannelId.ToString(),
                        Name = playlist.Title,
                        CoverArt = playlist.Thumbnails[playlist.Thumbnails.Count - 1].Url,
                    };

                    albums.Add(album);
                }

                ArtistAlbumsResponse albumsResponse = new()
                {
                    ArtistAlbums = albums,
                    HasError = false,
                    Error = ""
                };

                return albumsResponse;
            }
            catch (Exception)
            {
                throw;
            }
        }

        private static List<string> GetChannelPlaylistsIds(string channelId, string response)
        {
            List<string> ids = new List<string>();
            Regex exp = new("playlistId\":\"(.*?)\"");
            MatchCollection matches = exp.Matches(response);

            foreach (Match match in matches)
            {
                if (!ids.Contains(match.Groups[1].Value))
                {
                    ids.Add(match.Groups[1].Value);
                }
            }

            return ids;
        }

        public static List<string> GetChannelPlaylistsThumbnails(string channelId, string response)
        {
            List<string> thumbnails = new List<string>();
            Regex exp = new Regex("thumbnails\":\\[{\"url\":\"(.*?)\"");
            MatchCollection matches = exp.Matches(response);

            foreach (Match match in matches)
            {
                if (!thumbnails.Contains(match.Groups[1].Value) && match.Groups[1].Value.Contains("hqdefault"))
                {
                    thumbnails.Add(match.Groups[1].Value);
                }
            }

            return thumbnails;
        }

        public async Task<ArtistSongsResponse> GetArtistSongs(string artistId)
        {
            try
            {
                var contents = Client.Channels.GetUploadsAsync(artistId);
                List<Song> songs = new List<Song>();

                await foreach (var song in contents)
                {
                    songs.Add(new()
                    {
                        Id = song.Id,
                        ArtistId = song.Author.ChannelId.ToString(),
                        Name = song.Title,
                        CoverArt = song.Thumbnails.GetWithHighestResolution().Url,
                        Duration = song.Duration,
                        Url = song.Url,
                    });
                }

                ArtistSongsResponse response = new() { Songs = songs, Error = "", HasError = false };
                return response;
            }
            catch (Exception)
            {
                throw;
            }
        }

        public async Task<SuggestionsRespose> GetSuggestions(SuggestionsRequest suggestionsRequest)
        {
            Debug.WriteLine("GetSuggestionsStarted...");

            var tmp1 = suggestionsRequest.RawIntrests?.Split("|*|");
            if (tmp1 != null)
            {
                suggestionsRequest.Intrests = new();
                foreach (string item in tmp1)
                {
                    var tmp2 = item.Split("--)");
                    suggestionsRequest.Intrests.Add(new Interest() { Name = tmp2[0], Priority = int.Parse(tmp2[1]) });
                }
            }
            
            //suggestionsRequest.Intrests = new()
            //{
            //    new() { Name = "jacob's piano", Priority = 10 },
            //    new() { Name = "piano", Priority = 2 },
            //    new() { Name = "cello", Priority = 6 },
            //    new() { Name = "piano guys", Priority = 8 },
            //    new() { Name = "guitar", Priority = 3 },
            //    new() { Name = "violin", Priority = 5 },
            //    new() { Name = "viola", Priority = 1 },
            //};

            suggestionsRequest.Intrests.Sort((x, y) => y.Priority.CompareTo(x.Priority));

            List<Artist> artists = new();
            List<Album> albums = new();
            List<Song> songs = new();

            Debug.WriteLine("Finished initializing...");

            try
            {
                List<Task> tasks = new();
                foreach (Interest interest in suggestionsRequest.Intrests.Take(3))
                {
                    tasks.Add(Task.Run(async () =>
                    {
                        SearchRequest request = new()
                        {
                            Query = interest.Name,
                            ArtistsCount = suggestionsRequest.ArtistsCount,
                            AlbumsCount = suggestionsRequest.AlbumsCount,
                            SongsCount = suggestionsRequest.SongsCount
                        };

                        SearchResponse response = await Search(request);
                        artists.AddRange(response.Artists);
                        albums.AddRange(response.Albums);
                        songs.AddRange(response.Songs);
                    }));
                }

                Debug.WriteLine("Created Tasks...");

                await Task.WhenAll(tasks);

                Debug.WriteLine("Tasks Completed...");

                return new SuggestionsRespose()
                {
                    Artists = artists,
                    Albums = albums,
                    Songs = songs,
                    HasError = false,
                    Error = ""
                };
            }
            catch (Exception)
            {
                throw;
            }
        }

        public async Task<string> GetArtistSubscriberCount(string youtubeResponse)
        {
            return await Task.Run(async () =>
            {
                HttpClient client = new();
                client.DefaultRequestHeaders.Add("Accept-Language", "en-US");
                HttpResponseMessage res = await client.GetAsync("https://www.youtube.com/channel/UClQPk2WbC23z3eogxPbbOjw");
                youtubeResponse = await res.Content.ReadAsStringAsync();

                Regex regex = new("\"subscriberCountText\":\\s*{\\s*\"accessibility\":\\s*{\\s*\"accessibilityData\":\\s*{\\s*\"label\":\\s*\".*?\"\\s*}\\s*},\\s*\"simpleText\":\\s*\"(.*?)\"");
                MatchCollection matches = regex.Matches(youtubeResponse);
                Debug.WriteLine($"matches.Count = {matches.Count}");
                return matches[0].Groups[1].Value;
            });
        }
    }
}
