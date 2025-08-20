from src.game import TriviaGame, load_questions_from_json


def play_game():
    game = TriviaGame()
    questions = load_questions_from_json()

    for q in questions:
        game.add_question(q["question"], q["options"], q["correct_index"])

    while game.has_more_questions():
        q = game.questions[game.current_question_index]
        print(f"\nPregunta {game.current_question_index + 1}: {q['question']}")
        for i, option in enumerate(q['options']):
            print(f"{i + 1}. {option}")

        while True:
            try:
                ans = int(input("Selecciona una opción (1-4): ")) - 1
                if ans not in range(4):
                    print("⚠️ Entrada inválida. Debe ser un número entre 1 y 4.")
                    continue
                break
            except ValueError:
                print("⚠️ Entrada inválida. Debe ser un número entre 1 y 4.")

        if game.answer_question(ans):
            print("✅ ¡Correcto!")
        else:
            print(f"❌ Incorrecto. La respuesta correcta era: {q['options'][q['correct_index']]}")

    print(f"\n🎉 Juego terminado. Tu puntaje final es: {game.get_score()}")


def main_menu():
    while True:
        print("\n=== Menú Principal ===")
        print("1. Jugar")
        print("2. Salir")

        choice = input("Selecciona una opción: ").strip()

        if choice == "1":
            play_game()
        elif choice == "2":
            print("👋 ¡Hasta la próxima!")
            break
        else:
            print("⚠️ Opción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    main_menu()


