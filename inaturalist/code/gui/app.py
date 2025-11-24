from flask import Flask, request, jsonify, render_template, session
import random

app = Flask(__name__)
app.secret_key = "afd5bb7659c5d0f2da6077c944b548bea8eea6c9d724a845923b5449b86d919e"

WORDS = ['gudrun', 'redmountain', 'alko', 'gufi', 'vulpera', 'arone', 'bison']


def evaluate_guess(guess, target):
    result = ["_"] * len(target)
    misplaced = []

    target_counts = {}
    for ch in target:
        target_counts[ch] = target_counts.get(ch, 0) + 1

    for i, ch in enumerate(guess):
        if ch == target[i]:
            result[i] = ch
            target_counts[ch] -= 1

    for i, ch in enumerate(guess):
        if result[i] == "_" and ch in target_counts and target_counts[ch] > 0:
            misplaced.append(ch)
            target_counts[ch] -= 1

    return result, misplaced


@app.route('/')
def index():
    return render_template('index.html')


@app.post("/new")
def new_game():
    word = random.choice(WORDS)
    session["target"] = word
    session["masked"] = ["_" if c != " " else " " for c in word]
    session["attempts"] = []

    return jsonify({
        "target_length": len(word),
        "masked": session["masked"]
    })


@app.post("/guess")
def guess():
    data = request.get_json() or {}
    attempt = data.get("word", "")

    if "target" not in session:
        return jsonify({"error": "No active game"}), 400

    target = session["target"]
    masked = session["masked"]

    if len(attempt) != len(target):
        return jsonify({"error": f"Expected {len(target)} chars"}), 400

    guess_list = list(attempt)
    target_list = list(target)

    new_masked, misplaced = evaluate_guess(guess_list, target_list)

    for i, ch in enumerate(new_masked):
        if ch != "_":
            masked[i] = ch

    session["masked"] = masked
    session["attempts"].append(attempt)

    victory = masked == target_list

    response = {
        "masked": masked,
        "incorrectly_placed": misplaced,
        "victory": victory,
        "message": f'You guessed "{attempt}".'
    }

    if victory:
        response["target"] = target

    return jsonify(response)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
