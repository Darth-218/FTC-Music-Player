namespace FTC_MusicPlayerAPI.Models
{
    public class AlbumSongsResponse : BaseResponse
    {
        public List<Song>? AlbumSongs { get; set; }
    }
}
