namespace FTC_MusicPlayerAPI.Models
{
    public class BaseResponse
    {
        public bool HasError { get; set; }
        public string? Error { get; set; }
    }
}
