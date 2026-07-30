from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
import uuid

client = PersistentClient(path="vector_db")

collection = client.get_or_create_collection(
    name="documents"
)

model = SentenceTransformer("all-MiniLM-L6-v2")


def store_chunks(chunks, filename):

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

def search_chunks(query: str, n_results=5):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results