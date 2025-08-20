import pytest
from src.app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Menú principal" in response.data.decode("utf-8")

def test_login_route(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert "Pantalla de login" in response.data.decode("utf-8")

def test_game_route(client):
    response = client.get("/game")
    assert response.status_code == 200
    assert "Pantalla de preguntas" in response.data.decode("utf-8")

def test_results_route(client):
    response = client.get("/results")
    assert response.status_code == 200
    assert "Pantalla de resultados" in response.data.decode("utf-8")
