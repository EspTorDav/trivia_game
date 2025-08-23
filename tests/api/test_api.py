import pytest
from flask import session
from src.api import api_bp
from src.game import TriviaGame, load_questions_from_json
from app import app  # o main.py según tu estructura


@pytest.fixture
def client():
    # Activar modo test de Flask
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_get_question_initializes_game(client):
    response = client.get("/api/question")
    data = response.get_json()

    assert response.status_code == 200
    assert "question" in data
    assert "options" in data
    assert isinstance(data["options"], list)


def test_answer_and_score_progress(client):
    # Inicializamos con la primera pregunta
    client.get("/api/question")

    # Enviamos una respuesta (ej: índice 0)
    response = client.post("/api/answer", json={"answer": 0})
    data = response.get_json()

    assert response.status_code == 200
    assert "correct" in data
    assert "score" in data
    assert "has_more" in data


def test_play_until_results(client):
    # Inicializar juego
    client.get("/api/question")

    # Simular responder todas las preguntas
    while True:
        q_response = client.get("/api/question").get_json()
        if "message" in q_response and q_response["message"] == "No hay más preguntas":
            break
        client.post("/api/answer", json={"answer": 0})

    # Ver resultados
    result_response = client.get("/api/results")
    result_data = result_response.get_json()

    assert result_response.status_code == 200
    assert "final_score" in result_data
    assert isinstance(result_data["final_score"], int)
