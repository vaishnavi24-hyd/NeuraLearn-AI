import os
from datetime import datetime
import pdfplumber
import PyPDF2

UPLOAD_DIR = "uploads"

def ensure_upload_dir():
    """Ensure the uploads directory exists."""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

def save_pdf(uploaded_file):
    """Saves a Streamlit UploadedFile to the uploads directory."""
    ensure_upload_dir()
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def extract_pdf_data(file_path):
    """
    Extracts text and metadata from a saved PDF file.
    Uses PyPDF2 for page count and pdfplumber for robust text extraction.
    """
    filename = os.path.basename(file_path)
    page_count = 0
    full_text = ""
    pages = []
    
    try:
        # Fast metadata extraction with PyPDF2
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            page_count = len(reader.pages)
            
        # Robust text extraction with pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    full_text += text + "\n\n"
                    pages.append({"page_number": i + 1, "text": text})
                    
    except Exception as e:
        print(f"Error extracting PDF data from {filename}: {e}")
        full_text = f"Error extracting text: {e}"
        
    return {
        "filename": filename,
        "path": file_path,
        "page_count": page_count,
        "text": full_text,
        "pages": pages,
        "upload_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
