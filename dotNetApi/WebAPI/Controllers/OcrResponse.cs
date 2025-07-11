namespace WebAPI.Controllers
{
    public class OcrResponse
    {
        public string Vin { get; set; } = default!;
        public double Confidence { get; set; }
    }
}