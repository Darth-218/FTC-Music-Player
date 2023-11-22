namespace FTC_MusicPlayerAPI.Models
{
    public class Song
    {
        public required string Id { get; set; }
        public string? ArtistId { get; set; }
        public required string Name { get; set; }
        public required string Url { get; set; }
        public required string CoverArt { get; set; }
        public required TimeSpan? Duration { get; set; }
    }
}
