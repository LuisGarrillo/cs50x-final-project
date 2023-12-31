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
        email = request.form.get("email").lower()

        if not birthday or not gender or not email:
            return render_template("register.html", status=5), 400
        
        email_valid = email_check(email)
        if not email_valid:
            return render_template("register.html", status=6), 400
        
        repeated_email = db.execute('select * from users where email = ?', email)
        if repeated_email:
            return render_template("register.html", status=7), 400
        
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
        posts = db.execute("select p.message, p.date, u.username, u.id from posts p join users u on u.id = p.userId where u.id = ? or u.id in (select c.connectionId from connections c where c.userId = ?) order by p.date desc, p.time desc", session["user_id"], session["user_id"])
        return render_template("index.html", posts=posts), 200
    
    except Exception:
        return render_template("apology.html"), 400
    

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        interests = db.execute("SELECT name FROM areas order by name")

        interest = request.form.get("interest")
        interest_query = ''

        if interest:
            print(interest)
            area = db.execute("SELECT id FROM areas WHERE name = ?", interest)

            if not area:
                return render_template("search.html",interests=interests, status=1), 200
            
            areaId = str(area[0]["id"])

            interest_query = ' and i.areaId = ' + areaId

        username = request.form.get("username")
        user_query = ''
        if username:

            if username.rfind("/'") != -1 or username.rfind("%") != -1:
                return render_template("search.html",interests=interests, status=2), 400

            username = str(username)
            user_query = ' and u.username like \'%' + username + '%\''

        sql = "select distinct u.id, u.username from users u  left join interests i on i.userId = u.id where not u.id = " + str(session["user_id"])

        sql += interest_query + user_query

        results = db.execute(sql)
        print(sql)
       
        if results:
            for result in results:
                user_interests = db.execute("select a.name from interests i join areas a on a.id = i.areaId where i.userId = ?", result["id"])
                result["interest"] = ""
                for interest in user_interests:
                    result["interest"] += interest["name"] + ", "
                result["interest"] = result["interest"].rstrip(", ")

        return render_template("search.html",interests=interests, search=True, results=results), 200 
        
    else:
        interests = db.execute("SELECT name FROM areas order by name")
        return render_template("search.html", interests=interests), 200
    

@app.route("/profile", methods=["GET", "POST"])
def profile():
    def set_profile():
        rows = db.execute("SELECT username, email FROM users WHERE id = ?", session["user_id"])
        user = rows[0]

        user_interests = db.execute("SELECT a.name FROM interests i join areas a on a.id = i.areaId WHERE i.userId = ?", session["user_id"])
        interests = db.execute("SELECT name FROM areas order by name")

        friends = db.execute("select u.id, u.username from users u join connections c on c.connectionId = u.id where c.userId = ?", session["user_id"])
        return user, user_interests, interests, friends

    if request.method == "POST":
        user, user_interests, interests, friends = set_profile()
        
        interest = request.form.get("interest")

        if not interest:
            return render_template(
            "profile.html", 
            user=user, 
            user_interests=user_interests, 
            interests=interests, 
            friends=friends,
            status=1
            ), 200
        
        area = db.execute("SELECT id FROM areas WHERE name = ?", interest)

        if not area:
            return render_template(
            "profile.html", 
            user=user, 
            user_interests=user_interests, 
            interests=interests, 
            friends=friends,
            status=2
            ), 200
        
        areaId = area[0]["id"]

        check = db.execute("select * from interests where userId = ? and areaId = ?", session["user_id"], areaId)

        if check:
            return render_template(
            "profile.html", 
            user=user, 
            user_interests=user_interests, 
            interests=interests, 
            friends=friends,
            status=3
            ), 200

        db.execute("INSERT INTO interests (userId, areaId) VALUES (?,?)", session["user_id"], areaId)
        user_interests = db.execute("SELECT a.name FROM interests i join areas a on a.id = i.areaId WHERE i.userId = ?", session["user_id"])
        return render_template(
            "profile.html", 
            user=user, 
            user_interests=user_interests, 
            interests=interests, 
            friends=friends
            ), 200
    
    else:
        user, user_interests, interests, friends = set_profile()
        
        return render_template(
            "profile.html", 
            user=user, 
            user_interests=user_interests, 
            interests=interests, 
            friends=friends
            ), 200
    

@app.route("/other_profile")
def other_profile():
    def set_profile(id):
        friends = False
        request_sent = False
        request_received = False

        rows = db.execute("SELECT username, email FROM users WHERE id = ?", id)
        user = rows[0]

        user_interests = db.execute("SELECT a.name FROM interests i join areas a on a.id = i.areaId WHERE i.userId = ?", id)
        interests = db.execute("SELECT name FROM areas order by name")

        user_friends = db.execute("select u.id, u.username from users u join connections c on c.connectionId = u.id where c.userId = ?", id)

        rows = db.execute("select id, date from connections where userId = ? and connectionId = ?", id, session["user_id"])
        if rows:
            friends = True
            user["date"] = rows[0]["date"]
        else:
            rows = db.execute("select id from friendRequest where senderId = ? and receiverId = ?", session["user_id"], id)
            if rows:
                request_sent = True
            else:
                rows = db.execute("select id from friendRequest where senderId = ? and receiverId = ?", id, session["user_id"])
                if rows:
                    request_received = True

        return user, user_interests, interests, user_friends, friends, request_sent, request_received
   
    id = request.args.get("userId")

    if int(id) == int(session["user_id"]):
        return redirect("/profile")

    user, user_interests, interests, user_friends, friends, request_sent, request_received = set_profile(id)

    return render_template(
        "other_profile.html", 
        user=user, 
        user_interests=user_interests, 
        interests=interests, 
        user_friends=user_friends,
        id=id,
        friends=friends,
        request_sent=request_sent,
        request_received=request_received
        ), 200


@app.route("/requests")
def requests():
    rows = db.execute("select username from users where id = ?", session["user_id"])
    user = rows[0]
    requests = db.execute("select u.username, u.id from users u join friendRequest f on f.senderId = u.id where f.receiverId = ?", session["user_id"])

    return render_template("requests.html", requests=requests, user=user), 200


@app.route("/send_request", methods=["GET", "POST"])
def send_request():
    if request.method == "POST":
        friend_id = request.form.get("userId")

        if not friend_id:
            return render_template("apology.html"), 400
        
        db.execute("INSERT INTO friendRequest (senderId, receiverId, date, time) VALUES (?,?, DATE('now'), TIME('now'))", session["user_id"], friend_id)

        return redirect("/other_profile?userId=" + friend_id)


@app.route("/accept_request", methods=["GET", "POST"])
def accept_request():
    if request.method == "POST":
        friend_id = request.form.get("userId")

        if not friend_id:
            return render_template("apology.html"), 400
        
        db.execute("INSERT INTO connections (userId, connectionId, date, time) VALUES (?,?, DATE('now'), TIME('now'))", session["user_id"], friend_id)
        db.execute("INSERT INTO connections (userId, connectionId, date, time) VALUES (?,?, DATE('now'), TIME('now'))", friend_id, session["user_id"])

        db.execute("delete from friendRequest where senderId = ? and receiverId = ?", session["user_id"], friend_id)
        db.execute("delete from friendRequest where senderId = ? and receiverId = ?", friend_id, session["user_id"])

        return redirect("/other_profile?userId=" + friend_id)


@app.route("/delete_friend", methods=["GET", "POST"])
def delete_friend():
    if request.method == "POST":
        friend_id = request.form.get("userId")

        if not friend_id:
            return render_template("apology.html"), 400
        
        db.execute("delete from connections where userId = ? and connectionId = ?", session["user_id"], friend_id)
        db.execute("delete from connections where userId = ? and connectionId = ?", friend_id, session["user_id"])

        return redirect("/other_profile?userId=" + friend_id)
    
@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        post = request.form.get("post")

        if not post or post.isspace():
            return render_template("apology.html"), 400
        
        if len(post) > 1000:
            return render_template("apology.html"), 400
        
        db.execute("INSERT INTO posts (userId, message, date, time) VALUES (?,?, DATE('now'), TIME('now'))", session["user_id"], post)

        return redirect("/")