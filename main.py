from src.game import TriviaGame


if __name__ == "__main__":
    game = TriviaGame()
    game.add_question("¿Capital de Francia?", ["Berlín", "Madrid", "París", "Lisboa"], 2)
    game.add_question("¿2 + 2?", ["3", "4", "5", "6"], 1)

    while game.has_more_questions():
        q = game.questions[game.current_question_index]
        print(f"\nPregunta {game.current_question_index + 1}: {q['question']}")
        for i, option in enumerate(q['options']):
            print(f"{i + 1}. {option}")
        try:
            ans = int(input("Selecciona una opción (1-4): ")) - 1
        except ValueError:
            print("Entrada inválida, se cuenta como incorrecta")
            ans = -1

        if game.answer_question(ans):
            print("¡Correcto!")
        else:
            print(f"Incorrecto. La respuesta correcta era: {q['options'][q['correct_index']]}")

    print(f"\nJuego terminado. Tu puntaje final es: {game.get_score()}")
