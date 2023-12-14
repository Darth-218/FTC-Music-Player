namespace FTC_MusicPlayerAPI.Models
{
    public class Song
    {
        public required string Id { get; set; }
        public string? ArtistId { get; set; }
        public required string Name { get; set; }
        public required string Url { get; set; }

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

        public required TimeSpan? Duration { get; set; }
    }
}
