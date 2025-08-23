from flask import Flask, render_template, request, redirect, url_for, session, flash
from src.game import TriviaGame, load_questions_from_json
from src.api import api_bp
import copy
from functools import wraps

app = Flask(__name__)
app.secret_key = "supersecretkey"

#Registrar blueprint
app.register_blueprint(api_bp)

# Usuarios en memoria
users = {"tester": "tester"}

# Carga de preguntas
all_questions = load_questions_from_json()


# --- Decorador para login ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Debes iniciar sesión para acceder a esta página")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# --- Funciones de manejo de juego en sesión ---
def get_game_from_session():
    state = session.get("game_state")
    if not state:
        return None
    game = TriviaGame()
    game.questions = state["questions"]
    game.current_score = state["current_score"]
    game.current_question_index = state["current_question_index"]
    return game

def save_game_to_session(game):
    session["game_state"] = {
        "questions": game.questions,
        "current_score": game.current_score,
        "current_question_index": game.current_question_index
    }


# --- Rutas ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            flash("Usuario ya existe")
            return redirect(url_for("register"))
        users[username] = password
        flash("Registro exitoso, ahora inicia sesión")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["user"] = username

            # Crear juego nuevo para el usuario
            game_instance = TriviaGame()
            for q in copy.deepcopy(all_questions):
                game_instance.add_question(q["question"], q["options"], q["correct_index"])
            save_game_to_session(game_instance)

            return redirect(url_for("game"))
        flash("Usuario o contraseña incorrectos")
        return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/game", methods=["GET", "POST"])
@login_required
def game():
    # Inicializar TriviaGame en sesión si no existe
    if "game_instance" not in session:
        session["game_instance"] = copy.deepcopy(all_questions)
        session["current_score"] = 0
        session["current_question_index"] = 0

    # Cargar datos de sesión
    game_instance = TriviaGame()
    game_instance.questions = session["game_instance"]
    game_instance.current_score = session.get("current_score", 0)
    game_instance.current_question_index = session.get("current_question_index", 0)

    if request.method == "POST":
        answer_index_str = request.form.get("answer")
        if answer_index_str is not None:
            try:
                answer_index = int(answer_index_str)
                game_instance.answer_current_question(answer_index)
            except ValueError:
                pass  # si no es un número válido, se ignora

            # Guardar progreso en sesión
            session["current_score"] = game_instance.current_score
            session["current_question_index"] = game_instance.current_question_index

            # Revisar si se terminó el juego
            if not game_instance.has_more_questions():
                return redirect(url_for("results"))

    # Obtener pregunta actual
    if game_instance.has_more_questions():
        question = game_instance.get_current_question()
    else:
        return redirect(url_for("results"))

    return render_template("game.html", question=question, game_instance=game_instance)


@app.route("/results")
@login_required
def results():
    
    # Obtener puntaje final
    current_score = session.get("current_score", 0)
    total_questions = len(session.get("game_instance", []))

    # Limpiar datos del juego
    session.pop("game_instance", None)
    session.pop("current_score", None)
    session.pop("current_question_index", None)

    return render_template("results.html", score=current_score, total=total_questions)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)




