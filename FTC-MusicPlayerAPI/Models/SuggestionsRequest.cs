namespace FTC_MusicPlayerAPI.Models
{
    public class SuggestionsRequest
    {
        public required List<Interest> Interests { get; set; }
        public int ArtistsCount { get; set; }
        public int AlbumsCount { get; set; }
        public int SongsCount { get; set; }
        public string? RawInterests { get; set; }
    }
}
