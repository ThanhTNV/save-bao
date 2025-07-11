import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

# Initialize the FastAPI app
app = FastAPI()

# Define the OCR endpoint
@app.post("/ocr")
async def process_image(file: UploadFile = File(...)):
    try:
        # Read image file into memory
        image_bytes = await file.read()
        nparr = np.fromstring(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # --- PREPROCESSING FOR LOW-QUALITY IMAGES ---
        #  Xử lý ảnh để cải thiện chất lượng OCR
        # 1. Convert to grayscale
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 2. Apply thresholding to get a binary image (black and white)
        # This helps the OCR engine distinguish text from the background.
        # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # 3. Apply some noise reduction (optional but recommended)
        # denoised = cv2.medianBlur(thresh, 3)
        # --- END OF PREPROCESSING ---

        # Perform OCR using Tesseract
        # The 'config' option can help improve accuracy
        # custom_config = r'--oem 3 --psm 6'
        # text = pytesseract.image_to_string(denoised, config=custom_config)

        # For demonstration purposes, we will simulate the OCR result
        # In a real scenario, you would use the OCR library to extract text from the image.
        vin = "50H-43210"

        # Return the extracted text as JSON
        return JSONResponse(content={"vin": vin.strip()})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

# To run the server: uvicorn main:app --reload