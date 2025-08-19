import json
from src.game import TriviaGame

if __name__ == "__main__":
    game = TriviaGame()

     # Cargar preguntas desde JSON
    try:
        with open("data/questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
            for q in questions:
                game.add_question(q["question"], q["options"], q["correct_index"])
    except FileNotFoundError:
        print("No se encontró el archivo de preguntas. Asegúrate de tener data/questions.json")
        exit(1)
    except Exception as e:
        print(f"Error al cargar preguntas: {e}")
        exit(1)

    # Juego en consola
    while game.has_more_questions():
        q = game.questions[game.current_question_index]
        print(f"\nPregunta {game.current_question_index + 1}: {q['question']}")
        for i, option in enumerate(q['options']):
            print(f"{i + 1}. {option}")
        
        valid_input = False
        while not valid_input:
            try:
                ans = int(input("Selecciona una opción (1-4): "))
                if 0 <= ans < 4:
                    valid_input = True
                else:
                    print("Opción inválida, por favor selecciona un número del 1 al 4.")
            except ValueError:
                print("Entrada inválida, se cuenta como incorrecta")
                ans = -1

        if game.answer_question(ans):
            print("¡Correcto!")
        else:
            print(f"Incorrecto. La respuesta correcta era: {q['options'][q['correct_index']]}")

    print(f"\nJuego terminado. Tu puntaje final es: {game.get_score()}")
