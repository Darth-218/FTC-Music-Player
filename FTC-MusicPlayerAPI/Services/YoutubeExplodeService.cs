using FTC_MusicPlayerAPI.Models;
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
            var response = new SearchResponse()
            {
                Artists = [],
                Albums = [],
                Songs = []
            };

            var artistsTask = Task.Run(async () =>
            {
                var rawArtists = Client.Search.GetChannelsAsync(request.Query);
                response.Artists = await rawArtists.Take(request.ArtistsCount).Select(rawArtist => new Artist(){
                    Id = rawArtist.Id.ToString(),
                    Name = rawArtist.Title,
                    CoverArt = rawArtist.Thumbnails.GetWithHighestResolution().Url,
                })
                    .ToListAsync();
            });

            var albumsTask = Task.Run(async () =>
            {
                var rawAlbums = Client.Search.GetPlaylistsAsync(request.Query);
                response.Albums = await rawAlbums.Take(request.AlbumsCount).Select(rawAlbum => new Album()
                {
                    Id = rawAlbum.Id.ToString(),
                    ArtistId = rawAlbum.Author == null ? null : rawAlbum.Author!.ChannelId.ToString(),
                    Name = rawAlbum.Title,
                    CoverArt = rawAlbum.Thumbnails.GetWithHighestResolution().Url,
                }).ToListAsync();
            });


            var songsTask = Task.Run(async () =>
            {
                var rawSongs = Client.Search.GetVideosAsync(request.Query);
                response.Songs = await rawSongs.Take(request.SongsCount).Select(rawSong => new Song()
                {
                    Id = rawSong.Id.ToString(),
                    ArtistId = rawSong.Author.ChannelId.ToString(),
                    Name = rawSong.Title,
                    CoverArt = rawSong.Thumbnails.GetWithHighestResolution().Url,
                    Duration = rawSong.Duration,
                    Url = rawSong.Url
                }).ToListAsync();
            });

            await Task.WhenAll(artistsTask, albumsTask, songsTask);
            return response;
        }

        public async Task<AudioUrlResponse> GetSongUrl(string songId)
        {
            var video = await Client.Videos.GetAsync(songId);
            var streamsManifest = await Client.Videos.Streams.GetManifestAsync(video.Id);

            var audioStreams = streamsManifest.GetAudioOnlyStreams();
            var bestAudioStream = audioStreams.FirstOrDefault();

            AudioUrlResponse response = new() { HasError = false, Error = "", Url = bestAudioStream!.Url };

            return response;
        }

        public async Task<AlbumSongsResponse> GetAlbumSongs(string albumId)
        {
            var contents = Client.Playlists.GetVideosAsync(albumId);
            var songs = await contents.Select(song => new Song()
            {
                Id = song.Id,
                ArtistId = song.Author.ChannelId.ToString(),
                Name = song.Title,
                CoverArt = song.Thumbnails.GetWithHighestResolution().Url,
                Duration = song.Duration,
                Url = song.Url,
            }).ToListAsync();
            
            AlbumSongsResponse response = new() { AlbumSongs = songs, Error = "", HasError = false };
            return response;
        }

        public async Task<ArtistAlbumsResponse> GetArtistAlbums(string artistId)
        {
            List<Album> albums = [];
            Console.WriteLine("Getting Playlists...");
            HttpClient client = new();
            var response =
                await client.GetAsync($"https://www.youtube.com/channel/{artistId}/playlists");
            var responseBody = await response.Content.ReadAsStringAsync();

            var ids = GetChannelPlaylistsIds(responseBody);

            Console.WriteLine($"ids.length = {ids.Count}");

            PlaylistClient playlistClient = new(new HttpClient());

            foreach (var t in ids)
            {
                var playlist = await playlistClient.GetAsync(t);
                Album album = new()
                {
                    Id = playlist.Id.ToString(),
                    ArtistId = playlist.Author!.ChannelId.ToString(),
                    Name = playlist.Title,
                    CoverArt = playlist.Thumbnails[^1].Url,
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

        private static List<string> GetChannelPlaylistsIds(string response)
        {
            List<string> ids = [];
            Regex exp = new("playlistId\":\"(.*?)\"");
            var matches = exp.Matches(response);

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
            List<string> thumbnails = [];
            var exp = new Regex("thumbnails\":\\[{\"url\":\"(.*?)\"");
            var matches = exp.Matches(response);

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
            var contents = Client.Channels.GetUploadsAsync(artistId);
            List<Song> songs = [];

            await foreach (var song in contents)
            {
                songs.Add(new Song
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

        public async Task<SuggestionsRespose> GetSuggestions(SuggestionsRequest suggestionsRequest)
        {
            Debug.WriteLine("GetSuggestionsStarted...");

            var tmp1 = suggestionsRequest.RawInterests?.Split("|*|");
            if (tmp1 != null)
            {
                suggestionsRequest.Interests = [];
                foreach (var item in tmp1)
                {
                    var tmp2 = item.Split("--)");
                    suggestionsRequest.Interests.Add(new Interest() { Name = tmp2[0], Priority = int.Parse(tmp2[1]) });
                }
            }

            suggestionsRequest.Interests.Sort((x, y) => y.Priority.CompareTo(x.Priority));

            List<Artist> artists = [];
            List<Album> albums = [];
            List<Song> songs = [];

            Debug.WriteLine("Finished initializing...");

            List<Task> tasks = [];
            tasks.AddRange(suggestionsRequest.Interests.Take(3)
                .Select(interest => Task.Run(async () =>
                {
                    SearchRequest request = new()
                    {
                        Query = interest.Name,
                        ArtistsCount = suggestionsRequest.ArtistsCount,
                        AlbumsCount = suggestionsRequest.AlbumsCount,
                        SongsCount = suggestionsRequest.SongsCount
                    };

                    var response = await Search(request);
                    artists.AddRange(response.Artists);
                    albums.AddRange(response.Albums);
                    songs.AddRange(response.Songs);
                })));

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

        public async Task<string> GetArtistSubscriberCount(string youtubeResponse)
        {
            return await Task.Run(async () =>
            {
                HttpClient client = new();
                client.DefaultRequestHeaders.Add("Accept-Language", "en-US");
                var res =
                    await client.GetAsync("https://www.youtube.com/channel/UClQPk2WbC23z3eogxPbbOjw");
                youtubeResponse = await res.Content.ReadAsStringAsync();

                Regex regex =
                    new(
                        "\"subscriberCountText\":\\s*{\\s*\"accessibility\":\\s*{\\s*\"accessibilityData\":\\s*{\\s*\"label\":\\s*\".*?\"\\s*}\\s*},\\s*\"simpleText\":\\s*\"(.*?)\"");
                var matches = regex.Matches(youtubeResponse);
                Debug.WriteLine($"matches.Count = {matches.Count}");
                return matches[0].Groups[1].Value;
            });
        }

        public async Task<List<Song>> GetArtistLatestRelease(string artistId)
        {
            var contents = Client.Channels.GetUploadsAsync(artistId);
            var rawLatestRelease = await contents.Take(3).ToListAsync();

            return rawLatestRelease.Select(raw => new Song()
                {
                    Id = raw.Id,
                    ArtistId = raw.Author.ChannelId.ToString(),
                    Name = raw.Title,
                    CoverArt = raw.Thumbnails.GetWithHighestResolution().Url,
                    Duration = raw.Duration,
                    Url = raw.Url,
                })
                .ToList();
        }
    }
}