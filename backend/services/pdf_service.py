
import fitz
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rapidocr import RapidOCR


# Initialize OCR engine once
ocr_engine = RapidOCR()


# ==========================================
# Extract selectable text from PDF
# ==========================================

def extract_text_from_pdf(file_path: str):

    reader = PdfReader(file_path)

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text() or ""

        extracted_pages.append({
            "page_number": page_number,
            "text": page_text.strip()
        })

    return extracted_pages


# ==========================================
# OCR scanned PDF pages
# ==========================================

def extract_text_using_ocr(file_path: str):

    pdf = fitz.open(file_path)

    extracted_pages = []

    try:
        for page_number, page in enumerate(pdf, start=1):

            # Render page as an image
            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2),
                alpha=False
            )

            image_bytes = pix.tobytes("png")

            # RapidOCR can process image bytes
            result = ocr_engine(image_bytes)

            if result and result.txts:
                page_text = "\n".join(result.txts)
            else:
                page_text = ""

            extracted_pages.append({
                "page_number": page_number,
                "text": page_text.strip()
            })

            print(
                f"OCR completed: Page {page_number} | "
                f"Characters: {len(page_text)}"
            )

    finally:
        pdf.close()

    return extracted_pages


# ==========================================
# Combined PDF text extraction
# ==========================================

def extract_pdf_content(file_path: str):

    normal_pages = extract_text_from_pdf(file_path)

    ocr_pages = extract_text_using_ocr(file_path)

    final_pages = []

    for normal_page, ocr_page in zip(normal_pages, ocr_pages):

        normal_text = normal_page["text"]
        ocr_text = ocr_page["text"]

        # Prefer normal extraction when available
        if len(normal_text) >= 30:
            final_text = normal_text
        else:
            final_text = ocr_text

        final_pages.append(
            f"[Page {normal_page['page_number']}]\n{final_text}"
        )

    return "\n\n".join(final_pages)


# ==========================================
# Split text into chunks
# ==========================================

def chunk_text(text: str):

    if not text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    return splitter.split_text(text)
