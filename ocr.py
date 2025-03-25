import os
import re
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import pdfplumber

# Load environment variables
load_dotenv()

# Get credentials from .env
azure_key = os.getenv("AZURE_OCR_KEY")
azure_endpoint = os.getenv("AZURE_ENDPOINT")

# Validate credentials
if not azure_key or not azure_endpoint:
    raise ValueError("❌ ERROR: Missing AZURE_OCR_KEY or AZURE_ENDPOINT from environment variables!")

# Initialize Azure OCR Client
client = DocumentAnalysisClient(azure_endpoint, AzureKeyCredential(azure_key))
print("✅ Azure OCR Client initialized successfully!")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using pdfplumber and Azure OCR if necessary, filtering out metadata."""
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"  # Use pdfplumber if text is readable
            else:
                print(f"⚠️ Page contains images, using OCR for {pdf_path}")
                text += extract_text_using_ocr(pdf_path)  # Use OCR if text is missing

    return filter_questions_and_answers(text.strip())

def extract_text_using_ocr(pdf_path):
    """Extract text using Azure OCR for scanned PDFs."""
    with open(pdf_path, "rb") as file:
        poller = client.begin_analyze_document("prebuilt-document", file)
        result = poller.result()

    # Extract text from recognized lines
    ocr_text = "\n".join([line.content for page in result.pages for line in page.lines])
    return filter_questions_and_answers(ocr_text)

def filter_questions_and_answers(text):
    """Filters out metadata like school name, student name, and extracts only questions and answers."""
    lines = text.split("\n")
    
    # Define patterns to filter metadata
    metadata_patterns = [
        r"school\s*name", r"student\s*name", r"subject", r"exam", r"date",
        r"class", r"roll\s*no", r"marks", r"total", r"semester"
    ]
    
    filtered_lines = [
        line for line in lines if not any(re.search(pattern, line, re.IGNORECASE) for pattern in metadata_patterns)
    ]

    return "\n".join(filtered_lines).strip()
#http://127.0.0.1:8000/evaluate/
#http://127.0.0.1:8000/