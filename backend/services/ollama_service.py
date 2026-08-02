import requests
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:1.7b"


def generate_answer(question, context):

    prompt = f"""
You are an AI assistant.

You are given document passages retrieved by semantic search.

Read the QUESTION carefully.

IMPORTANT:

- Answer ONLY the exact question asked.
- Do NOT answer a different but similar question.
- If the question asks about "column matrix", do NOT answer about "row matrix".
- If the question asks about "order of matrix", do NOT answer about "square matrix".
- Use ONLY the retrieved passages.
- Keep the answer short (2-4 sentences).

{context}

Question:
{question}

Answer:
"""

    start = time.time()

    response = requests.post(
    OLLAMA_URL,
    json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
)

    response.raise_for_status()

    elapsed = time.time() - start
    print(f"\nOllama Time: {elapsed:.2f} seconds")

    data = response.json()

    print("\n========== OLLAMA RESPONSE ==========")
    print(data)
    print("=====================================\n")

    answer = data.get("response", "").strip()

    if answer == "":
        print("⚠️ WARNING: Ollama returned an empty response.")

    return answer