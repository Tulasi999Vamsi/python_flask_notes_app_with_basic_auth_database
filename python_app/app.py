from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret123"

# ================= DATABASE CONFIG =================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================= MODELS =================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

# ================= LOGIN DECORATOR =================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ================= ROUTES =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username, password=password).first()

        if user:
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
    notes = Note.query.all()
    return render_template("index.html", notes=notes)


@app.route("/add", methods=["POST"])
@login_required
def add_note():
    content = request.form.get("note")
    if content:
        note = Note(content=content)
        db.session.add(note)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:id>")
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_note(id):
    note = Note.query.get_or_404(id)

    if request.method == "POST":
        note.content = request.form.get("note")
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", note=note)


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


def initialize_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", password="1234")
            db.session.add(admin)
            db.session.commit()

# Call it manually when app starts
initialize_db()


