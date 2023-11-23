namespace FTC_MusicPlayerAPI.Models
{
    public class User
    {
        public int Id { get; set; }
        public required string Username { get; set; }
        public required IEnumerable<Playlist> Playlists { get; set; }
        public required IEnumerable<Artist> FollowedArtists { get; set; }
        public required IEnumerable<Album> FollowedAlbums { get; set; }
    }
}
