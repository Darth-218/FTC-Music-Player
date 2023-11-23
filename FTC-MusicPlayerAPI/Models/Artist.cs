namespace FTC_MusicPlayerAPI.Models
{
    public class Artist
    {
        public required string Id { get; set; }
        public required string Name { get; set; }
        public required string CoverArt { get; set; }
        public IEnumerable<Album>? Albums { get; set; }
        public IEnumerable<Song>? Songs { get; set; }
    }
}
