using FTC_MusicPlayerAPI.Models;
using System.Diagnostics.Metrics;
using YoutubeExplode;
using YoutubeExplode.Common;

namespace FTC_MusicPlayerAPI.Services
{
    public class YoutubeExplodeService : IYoutubeService
    {
        private YoutubeClient client { get; set; } = new YoutubeClient();
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
                    var rawArtists = client.Search.GetChannelsAsync(request.Query);

                    await foreach (var rawArtist in rawArtists)
                    {
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
                    var rawAlbums = client.Search.GetPlaylistsAsync(request.Query);

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

                var rawSongs = client.Search.GetVideosAsync(request.Query);

                Task songsTask = Task.Run(async () =>
                {
                    int counter = 0;
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
                var video = await client.Videos.GetAsync(songId);
                var streamsManifest = await client.Videos.Streams.GetManifestAsync(video.Id);

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
                var contents = client.Playlists.GetVideosAsync(albumId);
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
            try
            {
                //var contents = client.Channels.Get
            }
            catch (Exception)
            {
                throw;
            }
        }

        public IEnumerable<Song> GetArtistSongs(string artistId)
        {
            throw new NotImplementedException();
        }
    }
}
