namespace FTC_MusicPlayerAPI.Models
{
    public class Playlist
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public required string Name { get; set; }
        public required IEnumerable<Song> Songs { get; set; }
    }
}
