import streamlit as st
from sentence_transformers import SentenceTransformer

# Cache the model to prevent reloading it on every run
@st.cache_resource
def load_embedding_model():
    """Loads the sentence transformer model."""
    # all-MiniLM-L6-v2 is a fast and lightweight model producing 384-dimensional embeddings
    return SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding_dimension():
    """Returns the dimensionality of the embedding vectors."""
    model = load_embedding_model()
    return model.get_sentence_embedding_dimension()

def generate_embeddings(chunks):
    """
    Generates vector embeddings for a list of text chunks.
    
    Args:
        chunks: List of dictionary chunks (generated from chunking_service).
        
    Returns:
        List of dictionaries with the original chunk data plus the embedding vector.
    """
    if not chunks:
        return []
        
    model = load_embedding_model()
    
    # Extract just the text from the chunks
    texts = [chunk.get("text", "") for chunk in chunks]
    
    # Encode all texts into embeddings
    # We use show_progress_bar=False because Streamlit handles the UI spinner
    embeddings = model.encode(texts, show_progress_bar=False)
    
    embedded_chunks = []
    for i, chunk in enumerate(chunks):
        # Create a new dict preserving the original chunk data and adding the embedding
        embedded_chunk = {
            "chunk_id": chunk.get("chunk_id"),
            "text": chunk.get("text"),
            "filename": chunk.get("filename"),
            "page_number": chunk.get("page_number"),
            "chunk_index": chunk.get("chunk_index"),
            "length": chunk.get("length"),
            "embedding": embeddings[i].tolist() # Convert NumPy array to standard Python list
        }
        embedded_chunks.append(embedded_chunk)
        
    return embedded_chunks
