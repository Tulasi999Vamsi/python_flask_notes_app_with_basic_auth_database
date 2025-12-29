from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret123"

notes = []

USER = {
    "username": "admin",
    "password": "1234"
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USER["username"] and password == USER["password"]:
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    return render_template("index.html", notes=notes)


@app.route("/add", methods=["POST"])
@login_required
def add_note():
    note = request.form.get("note")
    if note:
        notes.append(note)
    return redirect(url_for("home"))


@app.route("/delete/<int:index>")
@login_required
def delete_note(index):
    if 0 <= index < len(notes):
        notes.pop(index)
    return redirect(url_for("home"))


@app.route("/edit/<int:index>", methods=["GET", "POST"])
@login_required
def edit_note(index):
    if request.method == "POST":
        new_note = request.form.get("note")
        if new_note:
            notes[index] = new_note
        return redirect(url_for("home"))
    return render_template("edit.html", note=notes[index], index=index)


@app.route('/addNum', methods=['POST'])
def add_numbers():
    data = request.get_json()
    num1 = data.get('num1')
    num2 = data.get('num2')

    return jsonify({
        "num1": num1,
        "num2": num2,
        "sum": num1 + num2
    })


if __name__ == "__main__":
    app.run(debug=True)
