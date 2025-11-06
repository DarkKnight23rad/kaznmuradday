from flask import Flask, render_template, request, jsonify, redirect, url_for
import json, random

app = Flask(__name__)

# --- Загружаем вопросы ---
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# --- Хранилище очков (пока без базы, просто в памяти) ---
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

