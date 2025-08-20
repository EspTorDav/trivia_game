import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def test_index_route(client):
    res = client.get("/")
    assert res.status_code == 200

def test_login_route(client):
    res = client.get("/login")
    assert res.status_code == 200

def test_game_route_with_login(client):
    with client.session_transaction() as sess:
        sess["user"] = "tester"
    res = client.get("/game")
    assert res.status_code == 200

def test_results_route_with_login(client):
    with client.session_transaction() as sess:
        sess["user"] = "tester"
    res = client.get("/results")
    assert res.status_code == 200




