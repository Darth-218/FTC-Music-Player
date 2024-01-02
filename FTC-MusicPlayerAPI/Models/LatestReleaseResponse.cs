namespace FTC_MusicPlayerAPI.Models;

public class LatestReleaseResponse : BaseResponse
{
    public List<Song> LatestRelease { get; set; } = [];
}