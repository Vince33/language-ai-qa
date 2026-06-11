from dotenv import load_dotenv
load_dotenv()

import chromadb
from sentence_transformers import SentenceTransformer
from anthropic import Anthropic

# --- Configuration ---
# Using English side of Aguaruna-English parallel corpus (CC0 licensed)
# Source: OPUS bible-uedin corpus
# Note: Standard embedding models perform poorly on Aguaruna directly.
# English side used for embedding/retrieval. This is a known limitation
# documented in NOTES.md — production use requires indigenous language
# embedding models.
CORPUS_PATH = "data/bible-uedin.agr-en.en"
MAX_SENTENCES = 500  # Use a subset for initial testing

# --- Setup ---
client = Anthropic()
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def load_corpus(path, max_sentences=500):
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[:max_sentences]

def build_vector_store(sentences):
    collection = chroma_client.get_or_create_collection("aguaruna_bible")
    if collection.count() == 0:
        print(f"Embedding {len(sentences)} sentences...")
        embeddings = embedding_model.encode(sentences).tolist()
        collection.add(
            documents=sentences,
            embeddings=embeddings,
            ids=[f"doc_{i}" for i in range(len(sentences))]
        )
        print("Vector store built.")
    else:
        print(f"Vector store already exists with {collection.count()} documents.")
    return collection

def retrieve(collection, query, n_results=3):
    query_embedding = embedding_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    return results["documents"][0]

def generate(query, context_chunks):
    context = "\n".join(context_chunks)
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Answer the following question using only the provided context.
If the context does not contain enough information, say so clearly.

Context:
{context}

Question: {query}"""
        }]
    )
    return response.content[0].text

if __name__ == "__main__":
    # Load corpus
    sentences = load_corpus(CORPUS_PATH)
    print(f"Loaded {len(sentences)} sentences from corpus")

    # Build vector store
    collection = build_vector_store(sentences)

    # Test retrieval and generation
    query = "Who was the father of Isaac?"
    print(f"\nQuery: {query}")

    chunks = retrieve(collection, query, n_results=1)
    print(f"\nRetrieved context:")
    for chunk in chunks:
        print(f"  - {chunk}")

    response = generate(query, chunks)
    print(f"\nGenerated response:\n{response}")