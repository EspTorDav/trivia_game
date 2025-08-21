import pytest
from src.game import TriviaGame

# -----------------------
# Test: respuesta individual (acierto/fallo)
# -----------------------
@pytest.mark.parametrize(
    "question, options, correct_index, answer_index, expected_result, expected_score",
    [
        ("2+2=?", ["3", "4", "5", "6"], 1, 1, True, 10),           # acierto
        ("Capital de España?", ["Madrid", "Barcelona", "Sevilla", "Valencia"], 0, 1, False, 0), # fallo
        ("Color del cielo?", ["Rojo", "Verde", "Azul", "Amarillo"], 2, 2, True, 10), # acierto
    ]
)
def test_answer_current_question_single(question, options, correct_index, answer_index, expected_result, expected_score):
    game = TriviaGame()
    game.add_question(question, options, correct_index)
    
    result = game.answer_current_question(answer_index)
    
    assert result == expected_result
    assert game.get_score() == expected_score

# -----------------------
# Test: varias preguntas y puntaje acumulado
# -----------------------
def test_multiple_questions():
    game = TriviaGame()
    
    game.add_question("2+2?", ["3", "4", "5", "6"], 1)
    game.add_question("Capital de España?", ["Madrid", "Barcelona", "Sevilla", "Valencia"], 0)
    game.add_question("Color del cielo?", ["Rojo", "Verde", "Azul", "Amarillo"], 2)
    
    results = [
        game.answer_current_question(1),
        game.answer_current_question(1),
        game.answer_current_question(2)
    ]
    
    assert results == [True, False, True]
    assert game.get_score() == 20
