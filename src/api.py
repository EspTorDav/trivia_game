from flask import Blueprint, jsonify, request, session
from src.game import TriviaGame, load_questions_from_json

api_bp = Blueprint("api", __name__, url_prefix="/api")

# ⚡ Endpoint: obtener la siguiente pregunta
@api_bp.route("/question", methods=["GET"])
def get_question():
    if "game_instance" not in session:
        # Inicializar si no existe
        session["game_instance"] = load_questions_from_json()
        session["current_score"] = 0
        session["current_question_index"] = 0

    game_instance = TriviaGame(
        questions=session["game_instance"]
    )
    game_instance.current_score = session["current_score"]
    game_instance.current_question_index = session["current_question_index"]

    if not game_instance.has_more_questions():
        return jsonify({"message": "No hay más preguntas"}), 200

    return jsonify(game_instance.get_current_question()), 200


# ⚡ Endpoint: enviar respuesta
@api_bp.route("/answer", methods=["POST"])
def answer_question():
    data = request.get_json()
    if not data or "answer" not in data:
        return jsonify({"error": "Falta parámetro 'answer'"}), 400

    game_instance = TriviaGame(
        questions=session["game_instance"]
    )
    game_instance.current_score = session["current_score"]
    game_instance.current_question_index = session["current_question_index"]

    result = game_instance.answer_current_question(int(data["answer"]))

    # Guardar progreso en sesión
    session["current_score"] = game_instance.current_score
    session["current_question_index"] = game_instance.current_question_index

    return jsonify({
        "correct": result,
        "score": game_instance.current_score,
        "has_more": game_instance.has_more_questions()
    }), 200


# ⚡ Endpoint: obtener puntuación final
@api_bp.route("/results", methods=["GET"])
def get_results():
    return jsonify({
        "final_score": session.get("current_score", 0)
    }), 200
