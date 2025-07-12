import cv2
import numpy as np
import pytesseract
import re
import os

def test_ocr_from_file(image_path):
    """
    Processes a local image file to extract potential VINs using OCR
    and saves intermediate steps for debugging.
    """
    try:
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not read image from path: {image_path}")
            return

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join(output_dir, "1_grayscale.png"), gray)

        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        cv2.imwrite(os.path.join(output_dir, "2_threshold.png"), thresh)

        denoised = cv2.medianBlur(thresh, 3)
        cv2.imwrite(os.path.join(output_dir, "3_denoised.png"), denoised)

        # Tesseract configuration:
        # --oem 3: Default OCR Engine Mode
        # --psm 11: Sparse text. Find as much text as possible in no particular order.
        # -c tessedit_char_whitelist: Restrict characters to only uppercase letters and numbers.
        whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        custom_config = f'--oem 3 --psm 11 -c tessedit_char_whitelist={whitelist}'
        ocr_data = pytesseract.image_to_data(denoised, output_type=pytesseract.Output.DICT, config=custom_config)

        # --- Debugging: Print all detected words and their confidence ---
        all_words = []
        for i in range(len(ocr_data['text'])):
            text = ocr_data['text'][i].strip()
            conf = float(ocr_data['conf'][i])
            if text:
                all_words.append(f"'{text}' (Conf: {conf}%)")
        print("--- All Detected Words ---")
        print(" ".join(all_words))
        print("--------------------------\n")

        # --- VIN Matching Logic ---
        # Combine all detected text fragments and clean them up
        cleaned_text = re.sub(r'[^A-Z0-9]', '', "".join(ocr_data['text'])).upper()
        print(f"--- Cleaned text for matching: '{cleaned_text}' ---\n")

        # New regex for a pattern like '99H77060'
        # \d{2}   - two digits (99)
        # [A-Z]   - one letter (H)
        # \d{5}   - five digits (77060)
        vin_pattern = re.compile(r"(\d{2}[A-Z]\d{5})")
        matches = vin_pattern.finditer(cleaned_text)

        # Calculate a general confidence score for all detected words
        confident_words = [float(c) for c in ocr_data['conf'] if float(c) > 0]
        avg_conf = sum(confident_words) / len(confident_words) if confident_words else 0

        results = []
        for match in matches:
            vin = match.group(1)
            # Format the VIN to be more readable
            formatted_vin = f"{vin[0:2]}-{vin[2:4]}-{vin[4:]}"
            results.append({
                "vin": formatted_vin,
                "confidence": round(avg_conf / 100, 2)
            })

        print("--- OCR Results (VIN Pattern Matched) ---")
        if results:
            for res in results:
                print(f"  - VIN: {res['vin']}, Confidence: {res['confidence'] * 100:.2f}%")
        else:
            print("  No potential VINs found matching the pattern.")
        print("-------------------------------------------\n")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    image_to_test = "test_ocr.jpg"
    test_ocr_from_file(image_to_test) 