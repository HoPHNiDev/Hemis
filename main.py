import json
from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
from flask_cors import CORS
from rapidfuzz import fuzz, process
from loguru import logger

app = Flask(__name__)
CORS(app)

logger.add(
    f"logs.log",
    rotation="100 MB",
    retention="7 days",
    colorize=True,
    format="[{time}] | {level: ^8} | {name: ^15} | {function: ^15} | {line: ^3} | msg: {message}",
    level="DEBUG",
)


def load_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_questions(keys_only: bool = False):
    questions = load_questions("questions.json")
    logger.debug(f"Questions is {questions}")

    if keys_only:
        questions_with_keys = {}
        for subject, questions_list in questions.items():
            logger.debug(f"Subject is {subject}")
            subject_question = {}
            for question in questions_list:
                # logger.debug(f"Question is {question}")
                subject_question[question["question"]] = question["answers"][
                    question["correct_answer_id"]
                ]
            questions_with_keys[subject] = subject_question

        return questions_with_keys

    return questions


def parser(text: str):
    questions = get_questions(keys_only=True)

    results = [
        "================================================================",
        "FOUND ANSWERS IN FORMAT Q:A",
        "================================================================",
    ]

    question_positions = []
    not_sorted_questions = []
    for lang, questions in questions.items():
        for question, answer in questions.items():
            match = process.extractOne(
                question,
                text.split("\n"),
                scorer=fuzz.partial_ratio,
            )
            if match:
                if match[1] == 100:
                    index = text.find(question)  # Найти индекс совпадения
                    question_positions.append((index, question, answer, match[0], lang))
                elif match[1] >= 80:
                    not_sorted_questions.append((question, answer, match[0], lang))

    question_positions.sort(key=lambda x: x[0])

    for _, question, answer, matched_text, lang in question_positions:
        results.append({"question": question, "answer": answer})
    if not_sorted_questions:
        results.append(
            "================================================================"
        )
        results.append(
            "PARTIAL FOUND ANSWERS ABOVE (80%), USE THEM, IF YOU HAVE QUESTIONS WITHOUT ANSWERS"
        )
        results.append(
            "================================================================"
        )
    for question, answer, matched_text, lang in not_sorted_questions:
        results.append({"question": question, "answer": answer})

    logger.info(f"Parsed results: {results}")

    return results


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


@app.route("/parse", methods=["POST"])
def parse():
    data = request.json
    html = data.get("html")
    logger.info(f'GOT "POST" request with data: {data}')
    soup = BeautifulSoup(html, "html.parser")

    text = soup.text
    logger.debug(f'"POST" request with text: {text}')

    results = parser(text=text)

    return jsonify(results)


@app.route("/", methods=["GET"])
def home():
    logger.info("GET homepage request received")
    return render_template("home.html")


@app.route("/questions", methods=["GET"])
def question_page():
    logger.info("GET questions request received")
    questions = get_questions()

    return render_template("questions.html", questions=questions)


@app.route("/questions", methods=["POST"])
def update_questions():
    data = request.json
    logger.debug(data)
    subject = data.get("subject")
    new_questions = data.get("new_questions")

    save_to_json_file(subject, new_questions)

    return {"status": "success"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5885)
