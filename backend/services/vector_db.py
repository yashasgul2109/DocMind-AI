from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
import uuid

client = PersistentClient(path="vector_db")

collection = client.get_or_create_collection(
    name="documents"
)

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def store_chunks(chunks, filename):

    # Remove ALL previously uploaded documents
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    embeddings = model.encode(chunks).tolist()

    ids = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(str(uuid.uuid4()))

        metadatas.append({
            "filename": filename,
            "chunk_number": i
        })

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

def search_chunks(query: str, n_results=10):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved = []

    for doc, meta, distance in zip(documents, metadatas, distances):
        retrieved.append({
            "document": doc,
            "metadata": meta,
            "distance": distance
        })

    retrieved.sort(key=lambda x: x["distance"])

    # Remove duplicate chunks
    unique_chunks = set()

    context = ""
    selected_metadata = []

    print("\n========== RETRIEVED CHUNKS ==========")

    for item in retrieved:

        chunk_no = item["metadata"]["chunk_number"]

        if chunk_no in unique_chunks:
            continue

        unique_chunks.add(chunk_no)

        print(
            f"Chunk: {chunk_no} | "
            f"Distance: {item['distance']:.4f}"
        )

        meta = item["metadata"]

        context += (
            f"{item['document']}\n\n"
        )

        selected_metadata.append(meta)

        # Keep only the best 3 UNIQUE chunks
        if len(selected_metadata) == 3:
            break

    print("======================================\n")

    return context, selected_metadata