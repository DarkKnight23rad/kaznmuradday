from flask import Flask, render_template, request, jsonify, redirect, url_for
import json, random

app = Flask(__name__)

# --- Загружаем вопросы ---
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# --- Хранилище очков ---
leaderboard = []

# --- Пароль ведущего ---
ADMIN_PASSWORD = "radiology2025"


@app.route("/")
def join():
    return render_template("join.html")


@app.route("/quiz")
def quiz():
    random.shuffle(questions)
    return render_template("quiz.html", questions=questions)


@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        score = data.get("score", 0)

        # сохраняем результат
        leaderboard.append({"name": name, "score": score})
        leaderboard.sort(key=lambda x: x["score"], reverse=True)

        return jsonify({"message": "Результаты получены!", "score": score})
    else:
        return render_template("results.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            return redirect(url_for("dashboard"))
        else:
            return render_template("admin_login.html", error="Неверный пароль")
    return render_template("admin_login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("host.html", questions=questions, leaderboard=leaderboard)


@app.route("/get_leaderboard")
def get_leaderboard():
    return jsonify(leaderboard)


@app.route("/get_questions")
def get_questions():
    return jsonify(questions)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
