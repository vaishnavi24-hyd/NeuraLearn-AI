import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_document(doc, chunk_size=1000, chunk_overlap=200):
    """
    Splits a document's extracted pages into semantic chunks.
    
    Args:
        doc: Dictionary containing 'filename' and 'pages' (list of dicts with 'page_number' and 'text').
        chunk_size: Maximum size of chunks to return.
        chunk_overlap: Overlap in characters between chunks.
        
    Returns:
        List of chunk dictionaries.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    
    chunks = []
    global_chunk_index = 0
    filename = doc.get("filename", "Unknown")
    
    # Check if 'pages' exists, otherwise fallback to 'text' (backward compatibility)
    if "pages" in doc and doc["pages"]:
        for page in doc["pages"]:
            page_num = page.get("page_number", 0)
            page_text = page.get("text", "")
            
            if not page_text.strip():
                continue
                
            page_chunks = text_splitter.split_text(page_text)
            
            for chunk_text in page_chunks:
                chunks.append({
                    "chunk_id": str(uuid.uuid4()),
                    "text": chunk_text,
                    "filename": filename,
                    "page_number": page_num,
                    "chunk_index": global_chunk_index,
                    "length": len(chunk_text)
                })
                global_chunk_index += 1
    else:
        # Fallback if no page level data
        full_text = doc.get("text", "")
        if full_text.strip():
            page_chunks = text_splitter.split_text(full_text)
            for chunk_text in page_chunks:
                chunks.append({
                    "chunk_id": str(uuid.uuid4()),
                    "text": chunk_text,
                    "filename": filename,
                    "page_number": "N/A",
                    "chunk_index": global_chunk_index,
                    "length": len(chunk_text)
                })
                global_chunk_index += 1
                
    return chunks
