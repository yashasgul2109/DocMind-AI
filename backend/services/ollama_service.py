
import requests
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:1.7b"


def generate_answer(question, context):

    if not context.strip():
        return "I couldn't find relevant information in the uploaded PDF."

    prompt = f"""
You are DocMind AI, a document question-answering assistant.

Answer the user's question using ONLY the supplied document context.

STRICT RULES:

1. The document context is your only source of factual information.
2. Do not use general knowledge to fill missing information.
3. Do not invent examples, facts, names or explanations.
4. Do not connect unrelated document information to the question.
5. If the context does not contain the answer, say:
   "This information was not found in the uploaded document."
6. If only partial information is available, clearly mention that.
7. Keep simple factual answers short.
8. Explain concepts only when the user asks for an explanation.
9. Do not create unrelated headings or sections.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

Answer using only the document context.
"""

    start = time.time()

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
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

    data = response.json()

    print(
        f"\nOllama Time: "
        f"{time.time() - start:.2f} seconds"
    )

    print("Done reason:", data.get("done_reason"))

    answer = data.get("response", "").strip()

    if not answer:
        return "The AI could not generate an answer. Please try again."

    print("\n========== FINAL ANSWER ==========")
    print(answer)
    print("==================================\n")

    return answer
