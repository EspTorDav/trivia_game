import pytest
from src.game import TriviaGame

# -----------------------
# Test: agregar y obtener preguntas
# -----------------------
def test_add_and_get_question():
    game = TriviaGame()
    game.add_question("Pregunta 1?", ["A","B","C","D"], 2)
    q = game.get_current_question()
    assert q["question"] == "Pregunta 1?"
    assert q["options"] == ["A","B","C","D"]

# -----------------------
# Test: has_more_questions
# -----------------------
def test_has_more_questions():
    game = TriviaGame()
    game.add_question("P1", ["A","B","C","D"], 0)
    game.answer_current_question(0)
    assert game.has_more_questions() is False

# -----------------------
# Test: simulación de sesión + puntaje final
# -----------------------
def test_session_score_simulation():
    session = {}
    all_questions = [
        {"question": "P1?", "options":["A","B","C","D"], "correct_index": 1},
        {"question": "P2?", "options":["A","B","C","D"], "correct_index": 2}
    ]

    game_instance = TriviaGame()
    game_instance.questions = all_questions

    game_instance.answer_current_question(1)
    game_instance.answer_current_question(2)

    session["current_score"] = game_instance.current_score
    session["current_question_index"] = game_instance.current_question_index

    assert session["current_score"] == 20  # 10 pts por cada correcta
    assert not game_instance.has_more_questions()

