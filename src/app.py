from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "Menú principal (placeholder)"

@app.route("/login")
def login():
    return "Pantalla de login (placeholder)"

@app.route("/game")
def game():
    return "Pantalla de preguntas (placeholder)"

@app.route("/results")
def results():
    return "Pantalla de resultados (placeholder)"


if __name__ == "__main__":
    app.run(debug=True)
