namespace FTC_MusicPlayerAPI.Models
{
    public class Album
    {
        public required string Id { get; set; }
        public required string? ArtistId { get; set; }
        public required string Name { get; set; }
        public required string CoverArt { get; set; }
        public List<Song>? Songs { get; set; }
    }
}
