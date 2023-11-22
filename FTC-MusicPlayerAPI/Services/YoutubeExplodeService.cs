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
                        counter++;
                        response.Artists.Add(new Artist()
                        {
                            Id = rawArtist.Id.ToString(),
                            Name = rawArtist.Title,
                            CoverArt = rawArtist.Thumbnails.GetWithHighestResolution().Url,
                        });

                        if (counter == request.ArtistsCount)
                        {
                            break;
                        }
                    }
                });

                Task albumsTask = Task.Run(async () =>
                {
                    int counter = 0;
                    var rawAlbums = client.Search.GetPlaylistsAsync(request.Query);

                    await foreach (var rawAlbum in rawAlbums)
                    {
                        counter++;
                        response.Albums.Add(new Album()
                        {
                            Id = rawAlbum.Id.ToString(),
                            ArtistId = rawAlbum.Author == null ? null : rawAlbum.Author!.ChannelId.ToString(),
                            Name = rawAlbum.Title,
                            CoverArt = rawAlbum.Thumbnails.GetWithHighestResolution().Url,
                        });

                        if (counter == request.AlbumsCount)
                        {
                            break;
                        }
                    }
                });

                var rawSongs = client.Search.GetVideosAsync(request.Query);

                Task songsTask = Task.Run(async () =>
                {
                    int counter = 0;
                    await foreach (var rawSong in rawSongs)
                    {
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

                        if (counter == request.SongsCount)
                        {
                            break;
                        }
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

        public string GetSongUrl(string songId)
        {
            throw new NotImplementedException();
        }

        public IEnumerable<Song> GetAlbumSongs(string albumId)
        {
            throw new NotImplementedException();
        }

        public IEnumerable<Album> GetArtistAlbums(string artistId)
        {
            throw new NotImplementedException();
        }

        public IEnumerable<Song> GetArtistSongs(string artistId)
        {
            throw new NotImplementedException();
        }
    }
}
