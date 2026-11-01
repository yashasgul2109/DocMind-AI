import fitz
import os
import uuid


IMAGE_FOLDER = "data/extracted_images"


def extract_images_from_pdf(pdf_path: str, filename: str):
    os.makedirs(IMAGE_FOLDER, exist_ok=True)

    pdf = fitz.open(pdf_path)
    extracted_images = []

    for page_index, page in enumerate(pdf):
        images = page.get_images(full=True)

        for image_info in images:
            xref = image_info[0]
            image_data = pdf.extract_image(xref)

            image_bytes = image_data["image"]
            image_ext = image_data["ext"]

            image_name = f"{uuid.uuid4().hex}.{image_ext}"
            image_path = os.path.join(IMAGE_FOLDER, image_name)

            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)

            extracted_images.append({
                "image_path": image_path,
                "filename": filename,
                "page_number": page_index + 1
            })

    pdf.close()
    return extracted_images