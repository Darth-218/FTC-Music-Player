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

        [HttpPost]
        [Route("")]
        public async Task<SearchResponse> Search(SearchRequest request)
        {
            return await _youtubeService.Search(request);
        }
    }
}
