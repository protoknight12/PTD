"""Critique: Flask app. Run: python app.py"""
import os
import secrets

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import db

app = Flask(__name__)
# ponytail: random fallback logs everyone out on restart; set SECRET_KEY in production.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.jinja_env.globals["TYPE_LABELS"] = {"movie": "Movie", "book": "Book", "music": "Album"}


@app.template_filter()
def compact(n):
    """142000 -> 142K, 2100000 -> 2.1M"""
    for size, suffix in ((1_000_000, "M"), (1_000, "K")):
        if n >= size:
            return f"{n / size:.1f}".removesuffix(".0") + suffix
    return str(n)


@app.template_filter()
def stars(rating):
    full = round(rating or 0)
    return "★" * full + "☆" * (5 - full)


@app.route("/")
def index():
    return render_template(
        "index.html",
        featured=db.get_featured(),
        rows=[
            ("movies", "Top Rated Movies", db.get_top_rated("movie")),
            ("books", "Top Rated Books", db.get_top_rated("book")),
            ("music", "Top Rated Albums", db.get_top_rated("music")),
        ],
        reviews=db.get_latest_reviews(),
    )


def validate_signup(name, email, password):
    if not 1 <= len(name) <= 100:
        return "Name must be 1-100 characters."
    if "@" not in email or len(email) > 254:
        return "Enter a valid email address."
    if not 8 <= len(password) <= 1024:
        return "Password must be at least 8 characters."
    return None


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html", form={})

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    error = validate_signup(name, email, password)
    user = None if error else db.create_user(name, email, generate_password_hash(password))
    if not error and not user:
        error = "An account with that email already exists."
    if error:
        return render_template("signup.html", form=request.form, error=error), 400
    log_in(user)
    return redirect(url_for("index"))


def log_in(user):
    session.clear()  # new session on login, so an old session id can't be reused
    session["user"] = {"id": user["id"], "name": user["name"]}


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", form={})

    email = request.form.get("email", "").strip()
    user = db.get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], request.form.get("password", "")):
        return render_template("login.html", form=request.form, error="Email or password is incorrect."), 400
    log_in(user)
    return redirect(url_for("index"))


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5500)
