from flask import Flask, render_template, request, jsonify
import json, random

app = Flask(__name__)

# Загружаем вопросы
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

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
        score = data.get("score", 0)
        return jsonify({"message": "Результаты получены!", "score": score})
    else:
        # при обычном заходе из браузера покажем HTML
        return render_template("results.html")

@app.route("/host")
def host():
    return render_template("host.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
