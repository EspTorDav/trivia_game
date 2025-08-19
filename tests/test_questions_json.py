import json
import os
import pytest

JSON_FILE = "data/questions.json"

def test_questions_json_exists():
    """Verifica que el archivo JSON existe"""
    assert os.path.exists(JSON_FILE), f"❌ No se encontró {JSON_FILE}"

def test_questions_json_structure():
    """Verifica que cada pregunta tiene el formato correcto"""
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
    
    assert isinstance(questions, list), "❌ El JSON debe ser una lista de preguntas"

    for i, q in enumerate(questions):
        assert "question" in q, f"❌ Pregunta {i+1} no tiene campo 'question'"
        assert "options" in q, f"❌ Pregunta {i+1} no tiene campo 'options'"
        assert "correct_index" in q, f"❌ Pregunta {i+1} no tiene campo 'correct_index'"

        assert isinstance(q["options"], list), f"❌ 'options' de la pregunta {i+1} debe ser una lista"
        assert len(q["options"]) == 4, f"❌ La pregunta {i+1} debe tener 4 opciones"
        assert 0 <= q["correct_index"] < 4, f"❌ 'correct_index' de la pregunta {i+1} debe estar entre 0 y 3"

def test_no_duplicate_questions():
    """Verifica que no hay preguntas repetidas en el JSON"""
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)

    seen_questions = set()
    duplicates = []

    for q in questions:
        text = q["question"].strip().lower()  # Ignora mayúsculas y espacios
        if text in seen_questions:
            duplicates.append(q["question"])
        else:
            seen_questions.add(text)

    assert not duplicates, f"❌ Preguntas duplicadas encontradas: {duplicates}"
