namespace WebAPI.Controllers
{
    public class OcrResult
    {
        public string Vin { get; set; } = default!;
        public double Confidence { get; set; }
    }

    public class OcrResponse
    {
        public List<OcrResult> Results { get; set; } = new();
    }
}