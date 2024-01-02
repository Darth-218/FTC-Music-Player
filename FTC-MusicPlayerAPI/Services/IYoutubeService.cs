using FTC_MusicPlayerAPI.Models;

namespace FTC_MusicPlayerAPI.Services
{
    public interface IYoutubeService
    {
        public Task<SearchResponse> Search(SearchRequest request);

        public Task<AudioUrlResponse> GetSongUrl(string songId);

        public Task<AlbumSongsResponse> GetAlbumSongs(string albumId);

        public Task<ArtistAlbumsResponse> GetArtistAlbums(string artistId);

        public Task<ArtistSongsResponse> GetArtistSongs(string artistId);

        public Task<string> GetArtistSubscriberCount(string youtubeResponse);

        public Task<SuggestionsRespose> GetSuggestions(SuggestionsRequest suggestionsRequest);
        
        public Task<List<Song>> GetArtistLatestRelease(string artistId);
        public Task<Artist> GetArtist(string artistId);
    }
}
