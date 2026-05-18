import json
import logging
import re
from langchain_community.llms import Ollama
from services.vector_store_service import query_database
from services.embedding_service import load_embedding_model

OLLAMA_MODEL = "mistral"
logger = logging.getLogger(__name__)

QUIZ_PROMPT_TEMPLATE = """You are NeuroLearn AI, an expert exam creator.
Generate a quiz based strictly on the provided Context Information.

Context Information:
---------------------
{context}
---------------------

Topic: {topic}
Number of Questions: {num_questions}
Difficulty: {difficulty}

Generate the quiz strictly as a JSON array of objects. Do not include any other text, markdown formatting like ```json, or explanations outside the JSON array.
Each object must have exactly these keys:
- "question": (string) The question text.
- "options": (array of strings) Exactly 4 possible options.
- "correct_answer": (string) The exact string from the options array that is correct.
- "explanation": (string) A brief explanation of why the answer is correct based on the context.

JSON Output:
"""

def clean_json_response(raw_text):
    """Attempt to clean the LLM output to extract just the JSON array."""
    cleaned = raw_text.strip()
    # Remove markdown formatting if present
    cleaned = re.sub(r'^```[jJ]son\s*', '', cleaned)
    cleaned = re.sub(r'^```\s*', '', cleaned)
    cleaned = re.sub(r'\s*```$', '', cleaned)
    
    # Try to find the first '[' and last ']'
    start_idx = cleaned.find('[')
    end_idx = cleaned.rfind(']')
    
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        return cleaned[start_idx:end_idx+1]
        
    return cleaned

def generate_quiz(topic, num_questions=3, difficulty="Intermediate"):
    """
    Retrieves context and generates a JSON-structured quiz.
    Returns a list of question dictionaries or None if it fails.
    """
    try:
        # 1. Embed query and retrieve
        model = load_embedding_model()
        query_vector = model.encode([topic])[0].tolist()
        retrieved_chunks = query_database(query_vector, n_results=5)
        
        valid_chunks = [c for c in retrieved_chunks if c['distance'] < 0.8]
        if not valid_chunks:
            return None # Insufficient context
            
        context_texts = [c['document'] for c in valid_chunks]
        context_string = "\n\n".join(context_texts)
        
        # 2. Build prompt
        prompt = QUIZ_PROMPT_TEMPLATE.format(
            context=context_string,
            topic=topic,
            num_questions=num_questions,
            difficulty=difficulty
        )
        
        # 3. Generate with Ollama
        logger.info(f"Generating quiz with {OLLAMA_MODEL}...")
        # Format "json" explicitly in the prompt above, but we rely on standard output parsing
        llm = Ollama(model=OLLAMA_MODEL, temperature=0.1)
        raw_output = llm.invoke(prompt)
        
        # 4. Parse JSON
        cleaned_json = clean_json_response(raw_output)
        quiz_data = json.loads(cleaned_json)
        
        # Ensure it's a list
        if isinstance(quiz_data, list) and len(quiz_data) > 0:
            return quiz_data
        return None
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM JSON output for quiz: {e}")
        logger.error(f"Raw Output was: {raw_output}")
        return None
    except Exception as e:
        logger.error(f"Quiz Generation Error: {e}")
        return None
