from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, password_check, email_check
# the code between the #- #- is from the CS50 Finance problem set

# credit to the cs50 team, love you guys! -

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finalProject.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

#-

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form.get("username")
        repeated_user = db.execute(
            "select username from users where username = ?", user
        )

        if repeated_user:
            return render_template("register.html", status=1), 400

        passw = request.form.get("password")
        confirm = request.form.get("confirmation")

        if not user or not passw or not confirm:
            return render_template("register.html", status=3), 400

        valid_pass = password_check(passw)

        if not valid_pass:
            return render_template("register.html", status=4), 400

        if passw != confirm:
            return render_template("register.html", status=2), 400
        new_hash = generate_password_hash(passw)

        birthday = request.form.get("birthday")
        gender = request.form.get("gender")
        email = request.form.get("email")

        if not birthday or not gender or not email:
            return render_template("register.html", status=5), 400
        
        email_valid = email_check(email)

        if not email_valid:
            return render_template("register.html", status=6), 400
        
        db.execute("insert into users (username, hash, birthday, gender, email) values(?,?,?,?,?)", user, new_hash, birthday, gender, email)

        result = db.execute("SELECT id FROM users WHERE username = ?", user)
        session["user_id"] = result[0]["id"]
        return redirect("/")
        
    else:
        return render_template("register.html"), 200

@app.route("/")
@login_required
def index():
    try:
        return render_template("index.html"), 400
    except Exception:
        return render_template("apology.html"), 400
    
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        pass
    else:
        return render_template("search.html"), 200
    
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        pass
    else:
        return render_template("profile.html"), 200
    
