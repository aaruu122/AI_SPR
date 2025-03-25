import os
import sys

# Ensure paths are absolute
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of ocr.py
QUESTION_PAPER_PATH = os.path.join(BASE_DIR, "chem_qp.pdf")
ANSWER_SHEET_PATH = os.path.join(BASE_DIR, "chem_ans.pdf")

# Debugging: Print paths
print(f"📂 Current Working Directory: {os.getcwd()}")
print(f"🔍 Checking: {QUESTION_PAPER_PATH}")
print(f"🔍 Checking: {ANSWER_SHEET_PATH}")

# File existence check
if not os.path.exists(QUESTION_PAPER_PATH):
    print(f"❌ ERROR: File not found - {QUESTION_PAPER_PATH}")
    sys.exit(1)  # Exit the script with an error

if not os.path.exists(ANSWER_SHEET_PATH):
    print(f"❌ ERROR: File not found - {ANSWER_SHEET_PATH}")
    sys.exit(1)  # Exit the script with an error

print("✅ Both files found. Proceeding with OCR...")

# --- OCR Code Here ---
try:
    from azure.ai.formrecognizer import DocumentAnalysisClient
    from azure.core.credentials import AzureKeyCredential

    # Azure credentials
    ENDPOINT = "YOUR_AZURE_OCR_ENDPOINT"
    API_KEY = "YOUR_AZURE_OCR_KEY"

    client = DocumentAnalysisClient(ENDPOINT, AzureKeyCredential(API_KEY))

    def extract_text(file_path):
        with open(file_path, "rb") as f:
            poller = client.begin_analyze_document("prebuilt-read", f)
            result = poller.result()
            extracted_text = "\n".join([line.content for page in result.pages for line in page.lines])
            return extracted_text

    question_text = extract_text(QUESTION_PAPER_PATH)
    answer_text = extract_text(ANSWER_SHEET_PATH)

    with open(os.path.join(BASE_DIR, "question_text.txt"), "w", encoding="utf-8") as q_file:
        q_file.write(question_text)

    with open(os.path.join(BASE_DIR, "answer_text.txt"), "w", encoding="utf-8") as a_file:
        a_file.write(answer_text)

    print("✅ OCR Extraction Completed Successfully!")

except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)