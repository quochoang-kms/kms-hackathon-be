import PyPDF2
import docx
import io
from fastapi import HTTPException, UploadFile

# Function to extract text from PDF
def extract_pdf_text(content: bytes, filename: str) -> str:
    try:
        pdf_file = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to extract text from PDF {filename}: {str(e)}"
        )

# Function to extract text from DOCX
def extract_docx_text(content: bytes, filename: str) -> str:
    try:
        doc_file = io.BytesIO(content)
        doc = docx.Document(doc_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to extract text from DOCX {filename}: {str(e)}"
        )


# Function to process file based on type
def process_file(content: bytes, file: UploadFile) -> str:
    """
    Process uploaded file and extract text based on file type
    
    Args:
        content: File content as bytes
        file: UploadFile object with filename info
        
    Returns:
        Extracted text from file
    """
    filename = file.filename.lower()
    
    if filename.endswith('.pdf'):
        return extract_pdf_text(content, file.filename)
    elif filename.endswith('.docx') or filename.endswith('.doc'):
        return extract_docx_text(content, file.filename)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.filename}. Please upload PDF or DOCX files only."
        )