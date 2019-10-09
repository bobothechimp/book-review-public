import os

from passlib.hash import sha256_crypt

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# engine = create_engine(os.getenv("postgres://plrueqrfqoawfm:dba8ea014066e4f18d3b8813c1f1e103b1a104d983303ffe92ad2c1ecca3ddab@ec2-54-235-246-201.compute-1.amazonaws.com:5432/d7kuluc1gil68"))

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html", unsuccessful='False')

@app.route("/registered", methods=["POST"])
def registered():
    un = request.form.get("username")
    pw = request.form.get("password")


    db.execute("BEGIN")

    prevUsers = db.execute("SELECT * FROM accounts WHERE username = :username", {"username": un}).fetchall()

    if prevUsers:
        db.execute("COMMIT")
        return render_template("signup.html", unsuccessful=True)
    else:
        db.execute("INSERT INTO accounts (username, password) VALUES (:username, :password)",
                     {"username": un, "password": hash_password(password=pw)})
        db.execute("COMMIT")
        return render_template("registered.html")

@app.route("/login")
def login():
    return render_template("login.html", unsuccessful=False)

@app.route("/logedin", methods=["POST"])
def logedin():
    un = request.form.get("username")
    pw = request.form.get("password")

    db.begin()

    storedPW = db.execute("SELECT password FROM accounts WHERE username = :username", {"username": un}).fetchone()

    db.commit()

    if(verify_password(storedPW[0], pw)):
        # TODO: set some sort of "loged in" variable to True
        return render_template("logedin.html")
    else:
        return render_template("login.html", unsuccessful=True)



def hash_password(password):

    return sha256_crypt.encrypt(password)






def verify_password(stored_password, provided_password):


    return sha256_crypt.verify(provided_password, stored_password)
