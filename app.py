from flask import Flask, flash, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Usuarios en memoria
users = {"tester":"tester"}

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

# Login
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
            return redirect(url_for("game"))
        flash("Usuario o contraseña incorrectos")
        return redirect(url_for("login"))
    return render_template("login.html")

# Juego
@app.route("/game")
def game():
    if "user" not in session:
        flash("Debes iniciar sesión para acceder a esta página")
        return redirect(url_for("login"))
    return render_template("game.html")

# Resultados
@app.route("/results")
def results():
    if "user" not in session:
        return redirect(url_for("login"))
    last_answer = session.get("last_answer", "No contestaste ninguna pregunta")
    return render_template("results.html", answer=last_answer)

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)



