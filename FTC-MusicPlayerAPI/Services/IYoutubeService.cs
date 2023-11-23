using FTC_MusicPlayerAPI.Models;

namespace FTC_MusicPlayerAPI.Services
{
    public interface IYoutubeService
    {
        public Task<SearchResponse> Search(SearchRequest request);

        public string GetSongUrl(string songId);

        public IEnumerable<Song> GetAlbumSongs(string albumId);

        public IEnumerable<Album> GetArtistAlbums(string artistId);

        public IEnumerable<Song> GetArtistSongs(string artistId);
    }
}
