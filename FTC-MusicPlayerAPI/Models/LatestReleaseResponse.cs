namespace FTC_MusicPlayerAPI.Models;

public class LatestReleaseResponse
{
    public List<Song> LatestRelease { get; set; } = [];
    public bool HasError { get; set; } = false;
    public string Error { get; set; } = "";
}