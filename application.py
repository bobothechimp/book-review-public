import os
import requests

from passlib.hash import sha256_crypt

from flask import Flask, session, render_template, request, jsonify, json
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



#Home page
@app.route("/")
def index():

    if session.get("currentUserID") is None:
        return render_template("index.html", logedin='False')
    else:
        return render_template("index.html", logedin='True')

#Sign up page
@app.route("/signup")
def signup():
    return render_template("signup.html", unsuccessful='False')

#Page for successful registration
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

#Log in page
@app.route("/login")
def login():
    return render_template("login.html", unsuccessful=False)

#Page for successful registration
@app.route("/loggedin", methods=["POST"])
def logedin():
    un = request.form.get("username")
    pw = request.form.get("password")

    db.execute("BEGIN")

    storedPW = db.execute("SELECT password FROM accounts WHERE username = :username", {"username": un}).fetchone()
    userID = db.execute("SELECT user_id FROM accounts WHERE username = :username", {"username": un}).fetchone()

    db.execute("COMMIT")

    if(verify_password(storedPW[0], pw)):
        # TODO: set some sort of "loged in" variable to True
        session["currentUserID"] = userID
        return render_template("loggedin.html")
    else:
        return render_template("login.html", unsuccessful=True)

#Logs user out of website
@app.route("/logout")
def logout():
    session["currentUserID"]=None
    return render_template("loggedout.html", logedin='False')

#Page for catalog of books
@app.route("/catalog")
def catalog():

    books = db.execute("SELECT * FROM books").fetchall();

    return render_template("catalog.html", books=books)

#Page showing search results in catalog
@app.route("/search", methods=["POST"])
def search():

    keyword = request.form.get("search")
    keyword = keyword.capitalize()

    results = db.execute("SELECT * FROM books WHERE title LIKE :keyword", {"keyword": "%" + keyword + "%"}).fetchall()

    return render_template("catalog.html", books=results)

#Page showing details about book
@app.route("/catalog/book/<string:isbn>")
def book(isbn):

    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn": isbn}).fetchone()
    reviews = db.execute("SELECT * FROM reviews WHERE isbn=:isbn", {"isbn": isbn}).fetchall()

    user = db.execute("SELECT username FROM accounts WHERE user_id=:id", {"id": session["currentUserID"][0]}).fetchone()
    userReview = db.execute("SELECT * FROM reviews WHERE poster=:user", {"user": user[0]}).fetchall()

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "9fK9b9a8syf0Al6ZSywKaA", "isbns": isbn})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    bookInfo = data["books"][0]

    if userReview is None:
        return render_template("catalogBook.html", book=book, reviews=reviews, info=bookInfo, canPost='True')
    else:
        return render_template("catalogBook.html", book=book, reviews=reviews, info=bookInfo, canPost='False')

#Posting a review for a book
@app.route("/catalog/book/<string:isbn>/post", methods=["POST"])
def post(isbn):

    review = request.form.get("review")

    print(session["currentUserID"])
    print(session["currentUserID"][0])


    db.execute("BEGIN")

    user = db.execute("SELECT username FROM accounts WHERE user_id=:id", {"id": session["currentUserID"][0]}).fetchone()

    db.execute("INSERT INTO reviews (poster, review_text, isbn) VALUES (:poster, :review_text, :isbn)", {"poster": user[0], "review_text": review, "isbn": isbn})

    db.execute("COMMIT")

    return book(isbn)

@app.route("/api/<string:isbn>")
def api(isbn):

    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return jsonify({"ERROR: Invalid book ISBN."}), 404

    count = db.execute("SELECT COUNT(*) FROM reviews WHERE isbn=:isbn", {"isbn": isbn}).fetchone()

    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": isbn,
        "review_count": count[0]
    })




#Function to hash passwords
def hash_password(password):

    return sha256_crypt.encrypt(password)

#Function to verify passwords
def verify_password(stored_password, provided_password):


    return sha256_crypt.verify(provided_password, stored_password)
