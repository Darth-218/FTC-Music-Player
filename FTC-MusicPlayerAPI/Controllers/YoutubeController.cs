using FTC_MusicPlayerAPI.Models;
using FTC_MusicPlayerAPI.Services;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;

namespace FTC_MusicPlayerAPI.Controllers
{
    [ApiController]
    [Route("[Controller]")]
    public class YoutubeController
    {
        IYoutubeService _youtubeService;
        public YoutubeController(IYoutubeService youtubeService)
        {
            _youtubeService = youtubeService;
        }

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
                return await _youtubeService.Search(request);
            }
            catch (Exception ex)
            {
                return new() { Artists = new(), Albums = new(), Songs = new(), HasError = true, Error = ex.Message };
            }
        }

        [HttpGet]
        [Route("/Youtube/GetAudioUrl")]
        public async Task<AudioUrlResponse> GetUrl(string id)
        {
            try
            {
                var response = await _youtubeService.GetSongUrl(id);
                return response;
            }
            catch (Exception ex)
            {
                return new() { HasError = true, Error = ex.Message, Url = "" };
            }
        }

        [HttpGet]
        [Route("/Youtube/GetAlbumSongs")]
        public async Task<AlbumSongsResponse> GetAlbumSongs(string id)
        {
            try
            {
                return await _youtubeService.GetAlbumSongs(id);
            }
            catch (Exception ex)
            {
                return new() { AlbumSongs = new(), HasError = true, Error = ex.Message };
            }
        }

        [HttpGet]
        [Route("/Youtube/GetArtistSongs")]
        public async Task<ArtistSongsResponse> GetArtistAlbums(string id)
        {
            try
            {
                return await _youtubeService.GetArtistSongs(id);
            }
            catch (Exception ex)
            {
                return new() { Songs = new(), HasError = true, Error = ex.Message };
            }
        }
    }
}
