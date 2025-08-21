import json
import os

class TriviaGame:
    def __init__(self, questions=None):
        self.questions = questions or []
        self.current_score = 0
        self.current_question_index = 0
        self.points_per_correct_answer = 10

    def add_question(self, question, options, correct_index):
        if len(options) != 4:
            raise ValueError("Se esperan 4 opciones.")
        self.questions.append({
            "question": question,
            "options": options,
            "correct_index": correct_index
        })

    def get_current_question(self):
        """Devuelve la pregunta actual para mostrar en la web"""
        if self.current_question_index >= len(self.questions):
            return None
        q = self.questions[self.current_question_index]
        return {
            "question": q["question"],
            "options": q["options"]
        }

    def answer_current_question(self, answer_index):
        """Registra respuesta y avanza a la siguiente pregunta"""
        if self.current_question_index >= len(self.questions):
            return None  # No hay más preguntas

        question = self.questions[self.current_question_index]
        correct = question["correct_index"] == answer_index

        if correct:
            self.current_score += self.points_per_correct_answer

        self.current_question_index += 1
        return correct

    def has_more_questions(self):
        return self.current_question_index < len(self.questions)

    def get_score(self):
        return self.current_score

def load_questions_from_json(file_path="data/questions.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError("❌ No se encontró el archivo de preguntas.")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convertimos cada pregunta en dict válido si hace falta
    questions = []
    for q in data:
        if "question" in q and "options" in q and "correct_index" in q:
            questions.append(q)
    return questions


