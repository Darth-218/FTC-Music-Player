using FTC_MusicPlayerAPI.Models;
using FTC_MusicPlayerAPI.Services;
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
        [Route("")]
        public async Task<SearchResponse> Search(string query)
        {
            SearchRequest request = new() 
            {
                Query = query,
                ArtistsCount = 1,
                AlbumsCount = 1,
                SongsCount = 20 
            };
            return await _youtubeService.Search(request);
        }
    }
}
