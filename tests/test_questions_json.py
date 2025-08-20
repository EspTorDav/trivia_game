import os
import pytest
from src.game import load_questions_from_json  # reutilizamos tu loader

JSON_FILE = "data/questions.json"

@pytest.fixture(scope="module")
def questions():
    assert os.path.isfile(JSON_FILE), f"❌ No se encontró {JSON_FILE}"
    return load_questions_from_json(JSON_FILE)

def test_questions_json_structure(questions):
    assert isinstance(questions, list) and len(questions) > 0, "❌ El JSON debe ser una lista con preguntas"
    for i, q in enumerate(questions, start=1):
        assert isinstance(q, dict), f"❌ La pregunta {i} no es un objeto"
        assert "question" in q, f"❌ Pregunta {i} no tiene 'question'"
        assert "options" in q, f"❌ Pregunta {i} no tiene 'options'"
        assert "correct_index" in q, f"❌ Pregunta {i} no tiene 'correct_index'"
        assert isinstance(q["options"], list), f"❌ 'options' de la pregunta {i} debe ser lista"
        assert len(q["options"]) == 4, f"❌ La pregunta {i} debe tener 4 opciones"
        assert isinstance(q["correct_index"], int), f"❌ 'correct_index' de la pregunta {i} debe ser int"

def test_valid_correct_index(questions):
    for q in questions:
        assert 0 <= q["correct_index"] < len(q["options"]), \
            f"❌ Índice fuera de rango en la pregunta: {q['question']}"

def test_no_duplicate_questions(questions):
    normalized = [q["question"].strip().lower() for q in questions]
    duplicates = {t for t in normalized if normalized.count(t) > 1}
    assert not duplicates, f"❌ Preguntas duplicadas encontradas: {duplicates}"
