import json
import logging
from langchain_community.llms import Ollama
from services.vector_store_service import query_database
from services.embedding_service import load_embedding_model
from services.quiz_service import clean_json_response # Reuse the JSON cleaner

OLLAMA_MODEL = "mistral"
logger = logging.getLogger(__name__)

FLASHCARD_PROMPT_TEMPLATE = """You are NeuroLearn AI, an expert study materials creator.
Extract key definitions, concepts, and relationships from the provided Context Information and format them as flashcards.

Context Information:
---------------------
{context}
---------------------

Topic Focus: {topic}
Number of Flashcards: {num_cards}

Generate the flashcards strictly as a JSON array of objects. Do not include any other text, markdown formatting like ```json, or explanations outside the JSON array.
Each object must have exactly these keys:
- "front": (string) The term, concept, or question (short and concise).
- "back": (string) The definition, explanation, or answer.

JSON Output:
"""

def generate_flashcards(topic, num_cards=5):
    """
    Retrieves context and generates a JSON-structured deck of flashcards.
    Returns a list of flashcard dictionaries or None if it fails.
    """
    try:
        # 1. Embed query and retrieve
        model = load_embedding_model()
        query_vector = model.encode([topic])[0].tolist()
        retrieved_chunks = query_database(query_vector, n_results=4)
        
        valid_chunks = [c for c in retrieved_chunks if c['distance'] < 0.8]
        if not valid_chunks:
            return None # Insufficient context
            
        context_texts = [c['document'] for c in valid_chunks]
        context_string = "\n\n".join(context_texts)
        
        # 2. Build prompt
        prompt = FLASHCARD_PROMPT_TEMPLATE.format(
            context=context_string,
            topic=topic,
            num_cards=num_cards
        )
        
        # 3. Generate with Ollama
        logger.info(f"Generating flashcards with {OLLAMA_MODEL}...")
        llm = Ollama(model=OLLAMA_MODEL, temperature=0.2)
        raw_output = llm.invoke(prompt)
        
        # 4. Parse JSON
        cleaned_json = clean_json_response(raw_output)
        flashcard_data = json.loads(cleaned_json)
        
        # Ensure it's a list
        if isinstance(flashcard_data, list) and len(flashcard_data) > 0:
            return flashcard_data
        return None
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM JSON output for flashcards: {e}")
        logger.error(f"Raw Output was: {raw_output}")
        return None
    except Exception as e:
        logger.error(f"Flashcard Generation Error: {e}")
        return None
