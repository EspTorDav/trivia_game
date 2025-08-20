from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session["user"] = username
            return redirect(url_for("game"))
    return render_template("login.html")

# Juego
@app.route("/game")
def game():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("game.html")

# Resultados
@app.route("/results")
def results():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("results.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)



