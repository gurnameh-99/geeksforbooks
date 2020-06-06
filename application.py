import os

from flask import Flask, session, render_template, redirect, url_for, request, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = 'i dont know'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        username = request.form.get("LoginUsr")
        password = request.form.get("LoginPass")

        if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 1:
            return redirect(url_for('home'))
        else:
            flash('invalid username or password', 'error')
            return redirect(url_for('index'))

@app.route("/register_1", methods=["POST"])
def register_1():
    name = request.form.get("nm")
    username = request.form.get("usrnm")
    email = request.form.get("em")
    password = request.form.get("pw")

    if(name == "" or username == "" or email == "" or password == ""):
        flash('Please fill all the required fields.', 'error')
        return redirect(url_for('register'))

    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0:
        db.execute("INSERT INTO users (name, username, email, password) VALUES (:name, :username, :email, :password)", {"name": name, "username": username, "email": email, "password": password})
        db.commit()
        return render_template("success.html")
    flash('user already registered.', 'error')
    return redirect(url_for('register'))

@app.route("/register")
def register():
    return render_template("register.html")
