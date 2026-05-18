import logging
from langchain_community.llms import Ollama
from services.vector_store_service import query_database
from services.embedding_service import load_embedding_model

# Force the usage of mistral as per requirements
OLLAMA_MODEL = "mistral"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Strict prompt template to force grounded answers and prevent hallucinations
RAG_PROMPT_TEMPLATE = """You are NeuroLearn AI, a highly intelligent and precise educational tutor. 
Your objective is to answer the student's question STRICTLY using ONLY the provided Context Information.

Context Information:
---------------------
{context}
---------------------

Student Question: {question}

Dynamic Formatting Controls:
- Explanation Complexity: {level}
- Teaching Style: {style}
- Output Length Constraint: Approximately {length} words.

Rules:
1. You must base your answer ONLY on the Context Information provided above.
2. If the Context Information does not contain the answer, you must state: "I don't have enough context in the uploaded documents to answer this." Do not attempt to guess or use outside knowledge.
3. Keep your answer clear, educational, and adhere to the Dynamic Formatting Controls.
4. Do not mention "Based on the context" or "According to the provided text". Just provide the answer directly.

Answer:
"""

def generate_rag_response(query, max_retrieval_results=8, controls=None):
    """
    Executes the full RAG pipeline: retrieves relevant chunks and generates a grounded answer.
    
    Args:
        query (str): The user's question.
        max_retrieval_results (int): Number of chunks to retrieve (increased for deeper context).
        controls (dict): Optional dict with 'level', 'length', and 'style' for dynamic prompting.
        
    Returns:
        dict: Contains 'answer' (str) and 'citations' (list of dicts).
    """
    if controls is None:
        controls = {
            "level": "Intermediate",
            "length": "Detailed Explanation",
            "style": "Standard"
        }
    try:
        # 1. Embed the query
        logger.info("Embedding user query...")
        model = load_embedding_model()
        query_vector = model.encode([query])[0].tolist()
        
        # 2. Retrieve relevant chunks from ChromaDB
        logger.info("Querying ChromaDB for semantic matches...")
        retrieved_chunks = query_database(query_vector, n_results=max_retrieval_results)
        
        # Fallback if nothing retrieved
        if not retrieved_chunks:
            return {
                "answer": "I don't have any uploaded documents in my knowledge core yet. Please commit vectors to the database first.",
                "citations": []
            }
            
        # Optional: Filter out weak retrievals based on distance. 
        # Chroma distance (cosine) ranges from 0 (perfect) to 2 (opposite).
        # We can set a threshold, e.g., > 0.9 distance means very weak.
        valid_chunks = [c for c in retrieved_chunks if c['distance'] < 0.9]
        
        if not valid_chunks:
            return {
                "answer": "I couldn't find any highly relevant information in the uploaded documents to answer this question securely.",
                "citations": retrieved_chunks  # Still return them for transparency debugging
            }

        # 3. Construct the Context String
        context_texts = []
        for chunk in valid_chunks:
            source = chunk['metadata'].get('filename', 'Unknown')
            page = chunk['metadata'].get('page_number', 'N/A')
            context_texts.append(f"[Source: {source}, Page: {page}]\n{chunk['document']}")
            
        context_string = "\n\n".join(context_texts)
        
        # 4. Build Prompt
        prompt = RAG_PROMPT_TEMPLATE.format(
            context=context_string, 
            question=query,
            level=controls.get('level', 'Intermediate'),
            style=controls.get('style', 'Standard'),
            length=controls.get('length', 'Detailed Explanation')
        )
        
        # 5. Generate Answer via Ollama
        logger.info(f"Invoking Ollama with model {OLLAMA_MODEL} and extended context length...")
        llm = Ollama(model=OLLAMA_MODEL, temperature=0.1, num_predict=2048) # Allow much longer detailed explanations
        
        answer = llm.invoke(prompt)
        
        return {
            "answer": answer.strip(),
            "citations": valid_chunks
        }
        
    except Exception as e:
        logger.error(f"RAG Pipeline Error: {e}")
        return {
            "answer": f"System Error: The neural generation pipeline encountered an exception. Make sure Ollama is running the '{OLLAMA_MODEL}' model locally. Error details: {str(e)}",
            "citations": []
        }
