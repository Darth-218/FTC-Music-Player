namespace FTC_MusicPlayerAPI.Models
{
    public class Artist
    {
        public required string Id { get; set; }
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

        public string? SubscriberCount { get; set; }

        public IEnumerable<Album>? Albums { get; set; }
        public IEnumerable<Song>? Songs { get; set; }
    }
}
