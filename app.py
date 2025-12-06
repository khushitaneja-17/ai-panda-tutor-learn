from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import random

app = Flask(__name__)
app.secret_key = "panda-secret-key"

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "tables.json")

with open(DATA_PATH, "r") as f:
    TABLES = json.load(f)

HOME_PAGE = """
<!doctype html>
<html>
<head>
    <title>AI Panda Tutor</title>
    <style>
        body { font-family: Arial, sans-serif; background: #fefae0; text-align: center; }
        .card { margin: 50px auto; padding: 20px; width: 320px; background: #fff; border-radius: 12px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .panda { font-size: 60px; }
        button, select { padding: 8px 12px; margin-top: 10px; border-radius: 8px; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <div class="card">
        <div class="panda">🐼</div>
        <h2>AI Panda Tutor</h2>
        <p>Hello! I am your panda tutor. Let's learn tables together.</p>
        <form method="post" action="{{ url_for('start_quiz') }}">
            <label>Choose a table:</label><br>
            <select name="table_number" required>
                <option value="">--select--</option>
                <option value="2">Table of 2</option>
                <option value="3">Table of 3</option>
                <option value="4">Table of 4</option>
            </select><br>
            <button type="submit">Start</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    session.clear()
    return render_template_string(HOME_PAGE)

@app.route("/start", methods=["POST"])
def start_quiz():
    table_number = request.form.get("table_number")
    if table_number not in TABLES:
        return redirect(url_for("home"))
    questions = TABLES[table_number][:]
    random.shuffle(questions)
    session["table_number"] = table_number
    session["questions"] = questions
    session["index"] = 0
    session["score"] = 0
    return redirect(url_for("quiz"))

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "questions" not in session:
        return redirect(url_for("home"))
    questions = session["questions"]
    index = session.get("index", 0)
    table_number = session.get("table_number")
    score = session.get("score", 0)
    total = len(questions)
    if index >= total:
        return redirect(url_for("result"))
    question = questions[index]
    return f"<h1>Table of {table_number}</h1><p>{question['question']} = ?</p>"

@app.route("/result")
def result():
    if "questions" not in session:
        return redirect(url_for("home"))
    score = session.get("score", 0)
    total = len(session["questions"])
    return f"<h1>Great job!</h1><p>You scored {score}/{total}</p>"

if __name__ == "__main__":
    app.run(debug=True)
