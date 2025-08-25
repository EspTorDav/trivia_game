from flask import Blueprint, jsonify, request, session
from src.game import TriviaGame, load_questions_from_json

api_bp = Blueprint("api", __name__, url_prefix="/api")

#  Endpoint: login de usuarios
@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Faltan credenciales"}), 400

    # Simulación de autenticación
    if data["username"] == "admin" and data["password"] == "1234":
        return jsonify({"token": "fake-jwt-token"}), 200
    return jsonify({"error": "Credenciales inválidas"}), 401

# Endpoint: obtener todas las preguntas
@api_bp.route("/questions", methods=["GET"])
def get_all_questions():
    questions = load_questions_from_json()
    seen = set()
    duplicates = [q["question"] for q in questions if q["question"] in seen or seen.add(q["question"])]
    if duplicates:
        return jsonify({"error": f"Preguntas duplicadas: {duplicates}"}), 400
    return jsonify(questions), 200

# Endpoint: obtener la siguiente pregunta
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


# Endpoint: enviar respuesta
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

# Endpoint: guardar puntuación
@api_bp.route("/score", methods=["POST"])
def save_score():
    data = request.get_json()
    if not data or "user" not in data or "score" not in data:
        return jsonify({"error": "Faltan parámetros"}), 400

    # Simulación de guardado (en el futuro: DB)
    return jsonify({
        "message": f"Puntuación de {data['user']} guardada",
        "score": data["score"]
    }), 200

# Endpoint: obtener puntuación final
@api_bp.route("/results", methods=["GET"])
def get_results():
    return jsonify({
        "final_score": session.get("current_score", 0)
    }), 200
