namespace FTC_MusicPlayerAPI.Models
{
    public class SearchRequest
    {
        public required string Query { get; set; }
        public required int ArtistsCount { get; set; }
        public required int AlbumsCount { get; set; }
        public required int SongsCount { get; set; }
    }
}
