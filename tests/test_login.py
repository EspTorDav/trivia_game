import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "testsecret"
    with flask_app.test_client() as client:
        flask_app.users = {"tester": "tester"}
        yield client

@pytest.fixture
def logged_in_client(client):
    with client.session_transaction() as sess:
        sess["user"] = "tester"
    return client

def test_login_success(client):
    response = client.post("/login", data={"username": "tester", "password": "tester"}, follow_redirects=True)
    assert "game" in response.get_data(as_text=True)

def test_login_failure(client):
    response = client.post("/login", data={"username": "tester", "password": "wrong"}, follow_redirects=True)
    assert "Usuario o contraseña incorrectos" in response.get_data(as_text=True)

def test_game_access_requires_login(client):
    response = client.get("/game", follow_redirects=True)
    assert "login" in response.get_data(as_text=True)

def test_game_access_with_login(logged_in_client):
    response = logged_in_client.get("/game")
    assert response.status_code == 200
