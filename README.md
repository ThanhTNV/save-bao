# Text Recognition Web Service

A web service that performs Optical Character Recognition (OCR) on low-quality text images using a combination of ASP.NET Core backend and Python-based AI processing.

## Project Overview

This project implements a web service that:
1. Receives images containing text through a REST API
2. Processes these images using advanced OCR techniques
3. Returns the extracted text data to the client

## Architecture

The system consists of two main components:

### ASP.NET Core Backend
- Handles HTTP requests and responses
- Manages file uploads
- Coordinates with the Python processing service
- Provides RESTful API endpoints

### Python AI Service
- Implements OCR using machine learning models
- Processes image data
- Performs text extraction and enhancement
- Handles image preprocessing and optimization

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

**Response:**
```json
{
    "success": true,
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
