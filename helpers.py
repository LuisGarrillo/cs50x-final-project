
from flask import redirect, render_template, session
from functools import wraps

import string

digits = string.digits
uppers = string.ascii_uppercase
lowers = string.ascii_lowercase


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def password_check(password):
    digit_check = False
    upper_check = False
    lower_check = False
    length_check = False

    # smooth way of checking if the password meets the requirements
    # https://stackoverflow.com/questions/6531482/how-to-check-if-a-string-contains-an-element-from-a-list-in-python

    if len(password) > 7:
        length_check = True
    if any(digit in password for digit in digits):
        digit_check = True
    if any(lower in password for lower in lowers):
        lower_check = True
    if any(upper in password for upper in uppers):
        upper_check = True

    if length_check and digit_check and upper_check and lower_check:
        return True
    else:
        return False
