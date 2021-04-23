import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# secret key
app.config['SECRET_KEY'] = 'secretkey8420'

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")

@app.route("/", methods=["GET", "POST"])
def index():
    # Get list of activities from database and display them on homepage
    if request.method == "POST":
        search = "%" + request.form.get("search") + "%"
        activities = db.execute("SELECT * FROM activities WHERE description LIKE :search OR title LIKE :search OR rating LIKE :search OR cost LIKE :search OR tag LIKE :search ORDER BY edit_date DESC", search=search)
        return render_template("index.html", activities=activities)
    activities = db.execute("SELECT * FROM activities ORDER BY edit_date DESC")
    return render_template("index.html", activities=activities)

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    tags = ["Culture/Heritage", "Educational", "Food", "Games/Board games", "Leisure", "Hiking", "Nature", "Sports", "Water Sports"]
    if request.method == "POST":
        title = request.form.get("title")
        unique_title = db.execute("SELECT title FROM activities WHERE title = ?", title)
        if len(unique_title) > 0:
            flash("Please fill in another title. Your title has already been used")
            return ("/")
        description = request.form.get("description")
        rating = float(request.form.get("rating"))
        tag = request.form.get("tag")
        cost = request.form.get("cost")
        if tag is None:
            db.execute("INSERT INTO activities (person_id, title, description, rating, cost) VALUES(?, ?, ?, ?, ?)", session["user_id"], title, description, rating, cost)
        else:
            db.execute("INSERT INTO activities (person_id, title, description, rating, tag, cost) VALUES(?, ?, ?, ?, ?, ?)", session["user_id"], title, description, rating, tag, cost)
        flash("Posted!")
        return redirect("/")

    return render_template("post.html", tags=tags)

@app.route("/profile")
@login_required
def profile():
    activities = db.execute("SELECT * FROM activities WHERE person_id = ? ORDER BY edit_date DESC", session["user_id"])
    return render_template("profile.html", activities=activities)

@app.route('/edit', defaults={'title':'title'}, methods=['GET','POST'])

@app.route("/edit/<title>", methods=['GET', 'POST'])
@login_required
def edit(title):
    if request.method == 'POST':
        new_title = request.form.get("title")
        description = request.form.get("description")
        rating = float(request.form.get("rating"))
        tag = request.form.get("tag")
        cost = request.form.get("cost")
        if tag is None:
            db.execute("UPDATE activities SET title = ?, description = ?, rating = ?, cost = ? WHERE title =?", new_title, description, rating, cost, title)
        else:
            db.execute("UPDATE activities SET title = ?, description = ?, rating = ?, tag = ?, cost = ? WHERE title = ? ", new_title, description, rating, tag, cost, title)
        flash('Post edited successfully!')
        return redirect("/")
    activity = db.execute("SELECT * FROM activities WHERE title = ? LIMIT 1", title)
    for activity in activity:
        title = activity["title"]
        description = activity["description"]
        cost = activity["cost"]
        rating = activity["rating"]
    tags = ["Culture/Heritage", "Games/Board games", "Leisure", "Hiking", "Nature", "Sports", "Water Sports"]
    return render_template('edit.html', title=title, description=description, cost=cost, rating=rating, tags=tags)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            session.clear()
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password of at least 8 characters")
            session.clear()
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password")
            session.clear()
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to home page
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Validate submission
        username = request.form.get("username")

        # Query database for username
        used_names = db.execute("SELECT * FROM users WHERE username = ?", username)

        if not username:
            flash("please enter a username")
            return redirect("/register")
        if len(used_names) > 0:
            flash("your username has been used. please choose another")
            return redirect("/register")

        password = request.form.get("password")

        confirmation = request.form.get("confirmation")

        if not password or len(password) < 8:
            flash("please enter a password of at least 8 characters")
            return redirect("/register")

        if not confirmation:
            flash("please fill in confirm password")
            return redirect("/register")

        if password != confirmation:
            flash("passwords do not match")
            return redirect("/register")

        user_id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        # Remember which user has logged in
        session["user_id"] = user_id

        flash("Registered")

        # Redirect user to home page where user is logged in
        return redirect("/")

    return render_template("register.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)