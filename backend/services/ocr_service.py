
from rapidocr import RapidOCR

# Initialize OCR engine
ocr_engine = RapidOCR()


def extract_text_from_image(image_path: str):
    result = ocr_engine(image_path)

    if not result or not result.txts:
        return ""

    extracted_text = "\n".join(result.txts)

    return extracted_text
