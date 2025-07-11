using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace WebAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class OcrController(IHttpClientFactory _httpClientFactory, IConfiguration _configuration) : ControllerBase
    {
        /// <summary>
        /// This endpoint is used to test the OCR functionality.
        /// </summary>
        /// <returns>A simple string indicating the OCR service is running.</returns>
        [HttpGet("health-check")]
        public IActionResult TestOcr()
        {
            return Ok("OCR service is running.");
        }
        // Additional OCR-related endpoints can be added here in the future.

        [HttpPost]
        public async Task<IActionResult> SanitizeImage(IFormFile file)
        {
            if (file == null || file.Length == 0)
            {
                return BadRequest("No file uploaded.");
            }
            var client = _httpClientFactory.CreateClient();

            // The URL of your running Python service
            var pythonApiUrl = _configuration["PYTHON_SERVICE_URL"] ?? throw new ArgumentNullException("Python service URL not found");

            // Use MultipartFormDataContent to send the file
            using var multipartFormContent = new MultipartFormDataContent();
            using var streamContent = new StreamContent(file.OpenReadStream());
            streamContent.Headers.ContentType = new MediaTypeHeaderValue(file.ContentType);

            multipartFormContent.Add(streamContent, name: "file", fileName: file.FileName);

            try
            {
                // Send the POST request to the Python API
                var response = await client.PostAsync(pythonApiUrl + "/ocr", multipartFormContent);

                if (response.IsSuccessStatusCode)
                {
                    // Read the JSON response from the Python API and return it
                    var result = await response.Content.ReadFromJsonAsync<OcrResponse>();
                    return Ok(result);
                }

                // If the Python API returned an error, forward that error
                return StatusCode((int)response.StatusCode, await response.Content.ReadAsStringAsync());
            }
            catch (HttpRequestException e)
            {
                // Handle network errors (e.g., Python server is down)
                return StatusCode(503, new { message = "The OCR service is unavailable.", details = e.Message });
            }
        }
    }
}
