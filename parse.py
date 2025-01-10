import json
from docx import Document
from pprint import PrettyPrinter
import requests


class DoubleQuotePrettyPrinter(PrettyPrinter):
    def format(self, obj, context, maxlevels, level):
        if isinstance(obj, str):  # Override string formatting
            return '"' + obj.replace('"', '\\"') + '"', True, False
        return super().format(obj, context, maxlevels, level)


def process_question_block(block):
    lines = block.split("====\n")
    question = lines[0].strip().replace("\n", " ")
    answers = [line.strip() for line in lines[1:] if line.strip()]
    correct = next(
        (idx for idx, ans in enumerate(answers) if ans.startswith("#")), None
    )
    answers = [ans.lstrip("#").strip().replace("\n=", "") for ans in answers]
    return question, answers, correct


def extract_questions_from_doc(doc):
    questions = []
    current_block = ""
    for para in doc.paragraphs:
        text = para.text.strip()
        if "++++" in text:  # End of a question block
            question, ans, correct = process_question_block(current_block)
            if question or ans:
                questions.append(
                    {"question": question, "answers": ans, "correct_answer_id": correct}
                )
            current_block = ""
        else:
            current_block += text + "\n"
    if current_block:
        question, ans, correct = process_question_block(current_block)
        if question and ans and correct:
            questions.append(
                {"question": question, "answers": ans, "correct_answer_id": correct}
            )
    return questions


def save_to_json_file(subject, new_questions, json_file="questions.json"):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if subject not in data:
        data[subject] = []
    data[subject].extend(new_questions)

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def send_new_questions(
    subject, new_questions, endpoint="http://127.0.0.1:5885/questions"
):
    headers = {"Content-Type": "application/json"}
    r = requests.post(
        endpoint,
        json={"subject": subject, "new_questions": new_questions},
        headers=headers,
    )
    if r.status_code == 200:
        return True


# Main logic
if __name__ == "__main__":
    document_path = input("Input path to document with questions >... ").strip()
    doc = Document(document_path)
    subject = input("Enter the subject name >...  ").strip()
    endpoint_url = (
        input(
            "Input flask endpoint URL, leave blank to use localhost(http://127.0.0.1:5885/questions) >... "
        )
        or "http://127.0.0.1:5885/questions"
    )

    extracted_questions = extract_questions_from_doc(doc)
    if send_new_questions(subject, extracted_questions, endpoint_url):
        print(
            f"Questions have been successfully saved to 'questions.json' under the subject '{subject}'."
        )
    else:
        print("Failed to send new questions to the server.")
