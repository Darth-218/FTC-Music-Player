using FTC_MusicPlayerAPI.Models;
using FTC_MusicPlayerAPI.Services;
using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;

namespace FTC_MusicPlayerAPI.Controllers
{
    [ApiController]
    [Route("[Controller]")]
    public class YoutubeController(IYoutubeService youtubeService)
    {
        [HttpGet]
        [Route("/Youtube/Search")]
        public async Task<SearchResponse> Search(string query, int artCount, int albCount, int sonCount)
        {

            SearchRequest request = new()
            {
                Query = query,
                ArtistsCount = artCount,
                AlbumsCount = albCount,
                SongsCount = sonCount
            };

            try
            {
                return await youtubeService.Search(request);
            }
            catch (Exception ex)
            {
                return new SearchResponse { Artists = [], Albums = [], Songs = [], HasError = true, Error = ex.Message };
            }
        }

        [HttpGet]
        [Route("/Youtube/GetAudioUrl")]
        public async Task<AudioUrlResponse> GetUrl(string id)
        {
            try
            {
                var response = await youtubeService.GetSongUrl(id);
                return response;
            }
            catch (Exception ex)
            {
                return new AudioUrlResponse { HasError = true, Error = ex.Message, Url = "" };
            }
        }

        [HttpGet]
        [Route("/Youtube/GetAlbumSongs")]
        public async Task<AlbumSongsResponse> GetAlbumSongs(string id)
        {
            try
            {
                return await youtubeService.GetAlbumSongs(id);
            }
            catch (Exception ex)
            {
                return new AlbumSongsResponse { AlbumSongs = [], HasError = true, Error = ex.Message };
            }
        }

        [HttpGet]
        [Route("/Youtube/GetArtistAlbums")]
        public async Task<ArtistAlbumsResponse> GetArtistAlbums(string id)
        {
            try
            {
                return await youtubeService.GetArtistAlbums(id);
            }
            catch (Exception ex)
            {
                return new ArtistAlbumsResponse { ArtistAlbums = [], HasError = true, Error = ex.Message };
            }
        }

        [HttpGet]
        [Route("/Youtube/GetArtistSongs")]
        public async Task<ArtistSongsResponse> GetArtistSongs(string id)
        {
            try
            {
                return await youtubeService.GetArtistSongs(id);
            }
            catch (Exception ex)
            {
                return new ArtistSongsResponse { Songs = [], HasError = true, Error = ex.Message };
            }
        }

        [HttpGet]
        [Route("/Youtube/GetArtist")]
        public async Task<string> GetArtist()
        {
            try
            {
                return await youtubeService.GetArtistSubscriberCount("");
            }
            catch (Exception ex)
            {
                Debug.WriteLine(ex.Message);
                return "";
            }
        }

        [HttpGet]
        [Route("/Youtube/GetSuggestions")]
        public async Task<SuggestionsRespose> GetSuggestions(int artCount, int albCount, int sonCount, string interests)
        {
            try
            {
                SuggestionsRequest request = new()
                {
                    ArtistsCount = artCount,
                    AlbumsCount = albCount,
                    SongsCount = sonCount,
                    Interests = [],
                    RawInterests = interests
                };
                return await youtubeService.GetSuggestions(request);
            }
            catch (Exception ex)
            {
                return new SuggestionsRespose { Albums = [], Artists = [], Songs = [], HasError = true, Error = ex.Message };
            }
        }

        [HttpGet]
        [Route("/Youtube/GetArtistLatestRelease")]
        public async Task<LatestReleaseResponse> GetArtistLatestRelease(string artistId)
        {
            try
            {
                return new LatestReleaseResponse
                    { LatestRelease = await youtubeService.GetArtistLatestRelease(artistId) };
            }
            catch (Exception ex)
            {
                return new LatestReleaseResponse { LatestRelease = [], HasError = true, Error = ex.Message };
            }
        }
    }
}
