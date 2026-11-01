
from services.ocr_service import extract_text_from_image

image_path = image_path = r"C:\Users\yasha\OneDrive\Desktop\Screenshot 2026-11-01 102911.png"

text = extract_text_from_image(image_path)

print("\n========== OCR RESULT ==========")
print(text)
print("================================")
