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

    # --- Test endpoint /api/answer con error ---
def test_answer_missing_parameter(client):
    response = client.post("/api/answer", json={})
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data


# --- Test endpoint /api/score ---
def test_save_score_success(client):
    response = client.post("/api/score", json={"user": "juan", "score": 5})
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Puntuación de juan guardada"
    assert data["score"] == 5


def test_save_score_missing_params(client):
    response = client.post("/api/score", json={"user": "juan"})
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data


# --- Test endpoint /api/questions ---
def test_get_all_questions(client):
    response = client.get("/api/questions")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert "question" in data[0]
    assert "options" in data[0]


# --- Test endpoint /api/login ---
def test_login_success(client):
    response = client.post("/api/login", json={"username": "admin", "password": "1234"})
    data = response.get_json()

    assert response.status_code == 200
    assert "token" in data


def test_login_invalid_credentials(client):
    response = client.post("/api/login", json={"username": "wrong", "password": "bad"})
    data = response.get_json()

    assert response.status_code == 401
    assert "error" in data


def test_login_missing_credentials(client):
    response = client.post("/api/login", json={})
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data

