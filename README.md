# Text Recognition Web Service

A web service that performs Optical Character Recognition (OCR) on low-quality text images using a combination of ASP.NET Core backend and Python-based AI processing.

## Project Overview

This project implements a web service that:
1. Receives images containing text through a REST API
2. Validates and sanitizes incoming requests for security
3. Processes these images using advanced OCR techniques
4. Returns the extracted text data to the client

## Architecture

The system consists of two main components:

### ASP.NET Core Backend
- Handles HTTP requests and responses
- Implements security measures:
  - Input validation and sanitization
  - File type verification
  - Size limit enforcement
  - Malware scanning
  - Request rate limiting
- Manages secure file uploads
- Coordinates with the Python processing service via secure internal communication
- Provides RESTful API endpoints with proper authentication and authorization

### Python AI Service
- Receives pre-validated images from ASP.NET Core service
- Implements OCR using machine learning models
- Processes image data
- Performs text extraction and enhancement
- Handles image preprocessing and optimization

## Data Flow

1. Client sends image to ASP.NET Core API
2. ASP.NET Core performs security checks:
   - Validates file format and size
   - Scans for malicious content
   - Authenticates request
3. If validation passes, image is forwarded to Python service
4. Python service processes image and returns extracted text
5. ASP.NET Core validates response and sends to client

## Prerequisites

- .NET 7.0 or later
- Python 3.8 or later
- Required Python packages (see `requirements.txt`)
- Visual Studio 2022 or VS Code with C# extensions

## Setup and Installation

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Install Python dependencies:
```bash
cd pthon
pip install -r requirements.txt
```

3. Build and run the ASP.NET Core application:
```bash
cd WebApi
dotnet build
dotnet run
```

## API Endpoints

### POST /api/ocr
Accepts image files and returns extracted text.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: Image file
- Max file size: 10MB
- Supported formats: jpg, png, bmp, tiff

**Response:**
```json
{
  "text": "Extracted text content",
  "confidence": 0.95
}
```

## Project Structure

```
├── WebApi/              # ASP.NET Core application
├── pthon/               # Python OCR service
│   ├── main.py         # Main Python processing script
│   └── requirements.txt # Python dependencies
└── README.md           # Project documentation
```
