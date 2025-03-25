import difflib
import csv

def evaluate_answers(questions, answers, csv_file_path="evaluation_results.csv"):
    """
    Evaluates answers by comparing them to questions, assigns marks, and saves results to CSV.

    Args:
        questions (list): List of question strings.
        answers (list): List of answer strings.
        csv_file_path (str): Path to save the CSV file.

    Returns:
        results (list): List of evaluation results.
        total_marks (int): Total score obtained.
    """
    total_marks = 0
    max_marks_per_question = 5
    results = []

    for i, (question, answer) in enumerate(zip(questions, answers)):
        if not question.strip() or not answer.strip():
            continue  # Skip empty or incomplete pairs

        similarity = difflib.SequenceMatcher(None, question.strip().lower(), answer.strip().lower()).ratio()
        marks = round(similarity * max_marks_per_question)
        total_marks += marks

        result = {
            "question_no": f"Q{i + 1}",
            "question": question.strip(),
            "student_answer": answer.strip(),
            "similarity_percentage": round(similarity * 100, 2),
            "marks_awarded": marks,
            "max_marks": max_marks_per_question
        }
        results.append(result)

    # Save results to CSV
    with open(csv_file_path, "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ["question_no", "question", "student_answer", "similarity_percentage", "marks_awarded", "max_marks"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)
        writer.writerow({
            "question_no": "Total",
            "question": "",
            "student_answer": "",
            "similarity_percentage": "",
            "marks_awarded": total_marks,
            "max_marks": len(results) * max_marks_per_question
        })

    print(f"✅ Evaluation completed! Results saved in '{csv_file_path}'.")
    return results, total_marks