from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
import uuid


# ==========================================
# ChromaDB Setup
# ==========================================

client = PersistentClient(path="vector_db")

collection = client.get_or_create_collection(
    name="documents"
)


# ==========================================
# Embedding Model
# ==========================================

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


# ==========================================
# Store PDF Chunks
# ==========================================

def store_chunks(chunks, filename):

    # ------------------------------------------
    # Validate chunks
    # ------------------------------------------

    if not chunks:
        raise ValueError(
            f"No text chunks were generated from '{filename}'. "
            "Please check PDF text extraction and chunking."
        )

    # Remove empty chunks
    chunks = [
        chunk.strip()
        for chunk in chunks
        if chunk and chunk.strip()
    ]

    if not chunks:
        raise ValueError(
            f"The PDF '{filename}' contains no usable text."
        )

    print("\n========== VECTOR DB ==========")
    print("Filename:", filename)
    print("Number of chunks:", len(chunks))
    print("First chunk:", repr(chunks[0][:300]))
    print("================================\n")


    # ------------------------------------------
    # Remove previously uploaded documents
    # ------------------------------------------

    existing = collection.get()

    if existing["ids"]:
        collection.delete(
            ids=existing["ids"]
        )


    # ------------------------------------------
    # Generate embeddings
    # ------------------------------------------

    embeddings = model.encode(
        chunks,
        show_progress_bar=True
    ).tolist()


    # ------------------------------------------
    # Validate embeddings
    # ------------------------------------------

    if not embeddings:
        raise ValueError(
            "Embedding generation returned an empty list."
        )

    if len(embeddings) != len(chunks):
        raise ValueError(
            f"Number of embeddings ({len(embeddings)}) "
            f"does not match number of chunks ({len(chunks)})."
        )


    # ------------------------------------------
    # Generate IDs and metadata
    # ------------------------------------------

    ids = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(
            str(uuid.uuid4())
        )

        metadatas.append({
            "filename": filename,
            "chunk_number": i
        })


    # ------------------------------------------
    # Store in ChromaDB
    # ------------------------------------------

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )


    print(
        f"Successfully stored {len(chunks)} chunks "
        f"from '{filename}' in ChromaDB."
    )


# ==========================================
# Search Similar Chunks
# ==========================================


def search_chunks(query: str, n_results=4):

    collection_data = collection.get()

    if not collection_data["ids"]:
        print("\nNo documents found in vector database.\n")
        return "", []

    # Generate query embedding
    query_embedding = model.encode(query).tolist()

    total_documents = len(collection_data["ids"])
    n_results = min(n_results, total_documents)

    # Retrieve only the most relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved = []

    for doc, meta, distance in zip(
        documents, metadatas, distances
    ):
        retrieved.append({
            "document": doc,
            "metadata": meta,
            "distance": distance
        })

    retrieved.sort(key=lambda x: x["distance"])

    context = ""
    selected_metadata = []

    print("\n========== RETRIEVED CHUNKS ==========")

    for item in retrieved:

        filename = item["metadata"].get("filename", "Unknown")
        chunk_number = item["metadata"].get("chunk_number", "?")

        print(
            f"\nFile: {filename} | "
            f"Chunk: {chunk_number} | "
            f"Distance: {item['distance']}"
        )

        context += (
            f"\n[File: {filename} | Chunk: {chunk_number}]\n"
            f"{item['document']}\n"
        )

        print(item["document"][:700])

        selected_metadata.append(item["metadata"])

    print("\n======================================\n")

    return context, selected_metadata
