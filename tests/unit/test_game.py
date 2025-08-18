import pytest
from src.game import TriviaGame

@pytest.mark.parametrize(
    "question, options, correct_index, answer_index, expected_result, expected_score",
    [
        # Caso 1: acierto
        ("2+2=?", ["3", "4", "5", "6"], 1, 1, True, 10),
        # Caso 2: fallo
        ("Capital de España?", ["Madrid", "Barcelona", "Sevilla", "Valencia"], 0, 1, False, 0),
        # Caso 3: otro acierto
        ("Color del cielo?", ["Rojo", "Verde", "Azul", "Amarillo"], 2, 2, True, 10),
    ]
)
def test_answer_question_single(question, options, correct_index, answer_index, expected_result, expected_score):
    game = TriviaGame()
    game.add_question(question, options, correct_index)
    
    result = game.answer_question(answer_index)
    
    assert result == expected_result
    assert game.get_score() == expected_score

def test_multiple_questions():
    game = TriviaGame()
    
    # Agregamos varias preguntas
    game.add_question("2+2?", ["3", "4", "5", "6"], 1)
    game.add_question("Capital de España?", ["Madrid", "Barcelona", "Sevilla", "Valencia"], 0)
    game.add_question("Color del cielo?", ["Rojo", "Verde", "Azul", "Amarillo"], 2)
    
    # Respuestas: acierto, fallo, acierto
    results = [game.answer_question(1), game.answer_question(1), game.answer_question(2)]
    
    assert results == [True, False, True]
    # Puntaje final: 10 + 0 + 10 = 20
    assert game.get_score() == 20
