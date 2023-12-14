namespace FTC_MusicPlayerAPI.Models
{
    public class Album
    {
        public required string Id { get; set; }
        public required string? ArtistId { get; set; }
        public required string Name { get; set; }

        private string? coverArt;
        public string? CoverArt
        {
            get => coverArt;
            set
            {
                if (value != null && !value!.Contains("https:"))
                {
                    coverArt = $"https:{value}";
                }
                else
                {
                    coverArt = value;
                }
            }
        }

        public List<Song>? Songs { get; set; }
    }
}
