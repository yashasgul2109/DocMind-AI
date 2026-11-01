
import requests
import base64
import time

from rapidocr import RapidOCR


OLLAMA_URL = "http://localhost:11434/api/generate"

TEXT_MODEL = "qwen3:1.7b"
VISION_MODEL = "qwen2.5vl:3b"

# Initialize OCR once
ocr_engine = RapidOCR()


# ==========================================
# OCR: Extract printed text
# ==========================================

def extract_text_from_image(image_path: str):

    result = ocr_engine(image_path)

    if not result or not result.txts:
        return ""

    return "\n".join(result.txts)


# ==========================================
# Text-based image questions
# ==========================================

def answer_from_ocr(extracted_text: str, question: str):

    if not extracted_text.strip():
        return "No readable printed text was detected in the image."

    prompt = f"""
You are DocMind AI, a document question-answering assistant.

Answer the user's question using ONLY the OCR text below.

STRICT RULES:
1. Use only information present in the OCR text.
2. Do not add general knowledge.
3. Do not invent examples or facts.
4. If the answer is present, answer directly.
5. If the answer is missing, say:
   "This information was not found in the image."
6. For lists, reproduce all relevant items.
7. For simple questions, keep answers concise.
8. Preserve the original meaning of the text.

OCR TEXT:
{extracted_text}

USER QUESTION:
{question}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": TEXT_MODEL,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "options": {
                "temperature": 0,
                "num_predict": 200,
                "num_ctx": 4096
            }
        },
        timeout=180
    )

    response.raise_for_status()

    return response.json().get("response", "").strip()


# ==========================================
# Visual questions
# ==========================================

def answer_from_vision(image_path: str, question: str):

    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    prompt = f"""
You are DocMind AI, an accurate image understanding assistant.

RULES:
1. Answer using only visible information.
2. Do not invent details.
3. Use OCR information only when clearly visible.
4. Explain diagrams and charts carefully.
5. If something is unclear, say so.
6. Keep the answer relevant to the question.

USER QUESTION:
{question}

Provide a clear answer.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": VISION_MODEL,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False,
            "options": {
                "temperature": 0,
                "num_predict": 300,
                "num_ctx": 4096
            }
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json().get("response", "").strip()


# ==========================================
# Main image question-answering function
# ==========================================

def generate_vision_answer(image_path: str, question: str):

    start = time.time()

    # STEP 1: Extract printed text
    extracted_text = extract_text_from_image(image_path)

    print("\n========== OCR EXTRACTED TEXT ==========")
    print(extracted_text)
    print("========================================\n")

    question_lower = question.lower()

    # STEP 2: Identify questions requiring visual understanding
    visual_keywords = [
        "diagram",
        "chart",
        "graph",
        "figure",
        "illustration",
        "visual",
        "what is shown",
        "describe this image",
        "describe the image",
        "explain the diagram",
        "explain the chart",
        "explain the graph"
    ]

    requires_vision = any(
        keyword in question_lower
        for keyword in visual_keywords
    )

    # STEP 3: Choose the appropriate model
    if extracted_text.strip() and not requires_vision:

        print("Processing with RapidOCR + Qwen3:1.7B")

        answer = answer_from_ocr(
            extracted_text,
            question
        )

    else:

        print("Processing with Qwen2.5-VL:3B")

        answer = answer_from_vision(
            image_path,
            question
        )

    elapsed = time.time() - start

    print(f"\nImage processing time: {elapsed:.2f} seconds")

    if not answer:
        return "The AI could not generate an answer. Please try again."

    return answer
