namespace FTC_MusicPlayerAPI.Models
{
    public class SuggestionsRespose
    {
        public required List<Artist> Artists { get; set; }
        public required List<Album> Albums { get; set; }
        public required List<Song> Songs { get; set; }
        public bool HasError { get; set; }
        public required string Error { get; set; }
    }
}
