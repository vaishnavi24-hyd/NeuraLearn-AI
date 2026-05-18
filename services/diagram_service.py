import re
import logging
from langchain_community.llms import Ollama

# Force the usage of mistral as per requirements
OLLAMA_MODEL = "mistral"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MERMAID_PROMPT = """You are NeuroLearn AI, a diagram generation expert. 
Your task is to analyze the provided Context Information and generate a Mermaid.js flowchart mapping out the core relationships, processes, or hierarchical structures related to the Student's Topic.

Context Information:
---------------------
{context}
---------------------

Student Topic: {topic}

Rules for Mermaid Generation:
1. Output ONLY valid Mermaid.js syntax. Do not include any conversational text, explanations, or markdown formatting blocks like ```mermaid.
2. Start the syntax with `graph TD;` (for top-down flowchart) or `graph LR;` (for left-right).
3. Use simple, clear node names. Avoid using parentheses or special characters inside node definitions unless enclosed in quotes (e.g., A["Step 1 (Start)"]).
4. Keep the diagram concise but informative (aim for 4 to 10 nodes).
5. If the context does not contain enough information to build a diagram, output exactly the string: NO_DIAGRAM

Output exactly the raw Mermaid code:
"""

KEY_POINTS_PROMPT = """Analyze the following Context Information and extract 3 to 4 concise, high-impact key points.
Return the output as a clean bulleted list. Do not include introductory text.

Context Information:
---------------------
{context}
---------------------

Key Points:
"""

def clean_mermaid_syntax(raw_syntax):
    """Strips markdown code blocks and cleans up common LLM syntax hallucinations."""
    if not raw_syntax:
        return "NO_DIAGRAM"
        
    cleaned = raw_syntax.strip()
    
    # Remove markdown code blocks
    cleaned = re.sub(r'^```[mM]ermaid\s*', '', cleaned)
    cleaned = re.sub(r'^```\s*', '', cleaned)
    cleaned = re.sub(r'\s*```$', '', cleaned)
    
    # Ensure it doesn't just return NO_DIAGRAM wrapped in something
    if "NO_DIAGRAM" in cleaned.upper():
        return "NO_DIAGRAM"
        
    return cleaned.strip()

def generate_diagram_syntax(topic, context_texts):
    """
    Generates Mermaid.js syntax based on the topic and context.
    
    Args:
        topic (str): The subject to visualize.
        context_texts (list): List of text chunks retrieved from ChromaDB.
        
    Returns:
        str: Raw Mermaid syntax or "NO_DIAGRAM".
    """
    try:
        context_string = "\n\n".join(context_texts)
        if not context_string.strip():
            return "NO_DIAGRAM"
            
        prompt = MERMAID_PROMPT.format(context=context_string, topic=topic)
        
        logger.info("Invoking Ollama for Mermaid generation...")
        llm = Ollama(model=OLLAMA_MODEL, temperature=0.1)
        raw_output = llm.invoke(prompt)
        
        return clean_mermaid_syntax(raw_output)
        
    except Exception as e:
        logger.error(f"Mermaid Generation Error: {e}")
        return "NO_DIAGRAM"

def extract_key_points(context_texts):
    """
    Extracts key points from the context for the visual dashboard.
    """
    try:
        context_string = "\n\n".join(context_texts)
        if not context_string.strip():
            return "No context available for key points."
            
        prompt = KEY_POINTS_PROMPT.format(context=context_string)
        
        llm = Ollama(model=OLLAMA_MODEL, temperature=0.2)
        return llm.invoke(prompt).strip()
        
    except Exception as e:
        logger.error(f"Key Points Extraction Error: {e}")
        return "Failed to extract key points."
