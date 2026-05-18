import os
import chromadb
from chromadb.config import Settings

# Define persistent storage path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
COLLECTION_NAME = "neurolearn_knowledge"

def get_db_client():
    """Initializes and returns a persistent ChromaDB client."""
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)
    return chromadb.PersistentClient(path=DB_PATH)

def get_collection():
    """Returns the main knowledge collection."""
    client = get_db_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"} # Cosine similarity works well for sentence-transformers
    )

def store_embeddings(embeddings_list):
    """
    Stores generated embeddings into ChromaDB.
    
    Args:
        embeddings_list: List of dictionaries containing embeddings and metadata.
    """
    if not embeddings_list:
        return 0
        
    collection = get_collection()
    
    ids = []
    embeddings = []
    documents = []
    metadatas = []
    
    for emb in embeddings_list:
        ids.append(emb["chunk_id"])
        embeddings.append(emb["embedding"])
        documents.append(emb["text"])
        metadatas.append({
            "filename": emb.get("filename", "Unknown"),
            "page_number": str(emb.get("page_number", "N/A")),
            "chunk_index": emb.get("chunk_index", 0)
        })
        
    # Upsert avoids duplicating chunks if they already exist
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    
    return len(ids)

def query_database(query_embedding, n_results=3):
    """
    Performs a semantic similarity search against the stored vectors.
    """
    collection = get_collection()
    
    # Query Chroma
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    # Structure the results for the UI
    structured_results = []
    if results["ids"] and len(results["ids"]) > 0:
        for i in range(len(results["ids"][0])):
            structured_results.append({
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i] if "distances" in results and results["distances"] else 0.0
            })
            
    return structured_results

def get_db_stats():
    """Returns database health and statistics."""
    try:
        collection = get_collection()
        count = collection.count()
        return {
            "status": "Online",
            "collection": COLLECTION_NAME,
            "total_vectors": count,
            "path": DB_PATH
        }
    except Exception as e:
        return {
            "status": f"Error: {str(e)}",
            "collection": COLLECTION_NAME,
            "total_vectors": 0,
            "path": DB_PATH
        }
