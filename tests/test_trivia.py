import pytest
from src.game import TriviaGame

# -----------------------
# Test 1: Agregar y obtener preguntas
# -----------------------
def test_add_and_get_question():
    game = TriviaGame()
    game.add_question("Pregunta 1?", ["A","B","C","D"], 2)
    q = game.get_current_question()
    assert q["question"] == "Pregunta 1?"
    assert q["options"] == ["A","B","C","D"]

# -----------------------
# Test 2: Respuesta correcta
# -----------------------
def test_answer_correct():
    game = TriviaGame()
    game.add_question("Pregunta 1?", ["A","B","C","D"], 1)
    correct = game.answer_current_question(1)
    assert correct is True
    assert game.current_score == game.points_per_correct_answer
    assert game.current_question_index == 1

# -----------------------
# Test 3: Respuesta incorrecta
# -----------------------
def test_answer_incorrect():
    game = TriviaGame()
    game.add_question("Pregunta 1?", ["A","B","C","D"], 0)
    correct = game.answer_current_question(2)
    assert correct is False
    assert game.current_score == 0
    assert game.current_question_index == 1

# -----------------------
# Test 4: has_more_questions
# -----------------------
def test_has_more_questions():
    game = TriviaGame()
    game.add_question("P1", ["A","B","C","D"], 0)
    game.answer_current_question(0)
    assert game.has_more_questions() is False

# -----------------------
# Test 5: Simulación sesión + puntuación final
# -----------------------
def test_session_score_simulation():
    session = {}
    all_questions = [
        {"question": "P1?", "options":["A","B","C","D"], "correct_index": 1},
        {"question": "P2?", "options":["A","B","C","D"], "correct_index": 2}
    ]

    game_instance = TriviaGame()
    game_instance.questions = all_questions

    # Responder todas
    game_instance.answer_current_question(1)
    game_instance.answer_current_question(2)

    # Guardar en sesión
    session["current_score"] = game_instance.current_score
    session["current_question_index"] = game_instance.current_question_index

    assert session["current_score"] == 20  # 10 pts por cada correcta
    assert not game_instance.has_more_questions()
