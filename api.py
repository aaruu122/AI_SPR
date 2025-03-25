from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from ocr import extract_text_from_pdf
from evaluate_answers import evaluate_answers
import os

app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "Server is running!"}

@app.post("/evaluate/")
async def evaluate(question_pdf: UploadFile = File(...), answer_pdf: UploadFile = File(...)):
    try:
        # Save uploaded PDFs
        question_path = f"temp_{question_pdf.filename}"
        answer_path = f"temp_{answer_pdf.filename}"

        with open(question_path, "wb") as q_file:
            q_file.write(await question_pdf.read())
        with open(answer_path, "wb") as a_file:
            a_file.write(await answer_pdf.read())

        # Extract text
        question_text = extract_text_from_pdf(question_path)
        answer_text = extract_text_from_pdf(answer_path)

        # Split the extracted text into individual lines/questions
        question_list = [line.strip() for line in question_text.split('\n') if line.strip()]
        answer_list = [line.strip() for line in answer_text.split('\n') if line.strip()]

        # Evaluate answers
        results, total_marks = evaluate_answers(question_list, answer_list)

        # Clean up temp files
        os.remove(question_path)
        os.remove(answer_path)

        return JSONResponse(content={
            "results": results,
            "total_marks": total_marks
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})