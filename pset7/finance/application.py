from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Query current user's cash
    userCash = db.execute("SELECT cash FROM users WHERE id = :userId",
                          userId=session["user_id"])

    # Transform number with usd() function
    userCash = usd(userCash[0]["cash"])

    # Query data and saves into "rows"
    # https://www.tutorialspoint.com/sqlite/sqlite_group_by.htm for more info
    rows = db.execute("SELECT stock, sum(shares), price, sum(price*shares) FROM transactions WHERE username = :username GROUP BY stock HAVING sum(shares) > 0 ORDER BY stock",
                        username=session["user_id"])

    # Tranform number with usd() function
    if rows != []:
        rows[0]["sum(price*shares)"] = usd(rows[0]["sum(price*shares)"])
        rows[0]["price"] = usd(rows[0]["price"])


    # Passes rows and userCash variables to html
    return render_template("index.html", rows=rows, userCash=userCash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    # Buy share
    if request.method == "POST":

        # Ensure symbol was provided
        if not request.form.get("symbol"):
            return apology("Must provide symbol", 400)

        # Ensure symbol exists
        elif lookup(request.form.get("symbol")) == None:
            return apology("Symbol does not exist", 400)

        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Please input an integer number", 400)

        # Ensure positive number of shares
        if shares < 1:
            return apology("N° of shares is not positive", 400)

        # Returns symbol requested
        symb = lookup(request.form.get("symbol"))

        # Saves symbol['price']
        price = symb['price']

        # Query current user's cash
        userCash = db.execute("SELECT cash FROM users WHERE id = :userId",
                                userId=session["user_id"])

        # Storing updated user's cash into newCash
        newCash = userCash[0]["cash"] - float((request.form.get("shares"))) * price

        # Ensure user has enough money to buy share * price
        if userCash[0]["cash"] < float((request.form.get("shares"))) * price:
            return apology("You don't have enough money prick", 400)
        else:
            # UPDATE current user cash in database
            db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",
                    user_id=session["user_id"],
                    cash=newCash)

        # INSERT row into database
        rows = db.execute("INSERT INTO transactions (username, stock, price, shares) VALUES (:username, :stock, :price, :shares)",
                        username=session["user_id"],
                        stock=symb['symbol'],
                        price=price,
                        shares=request.form.get("shares"),)

        # Pass a message to html. More info at (http://flask.pocoo.org/docs/0.12/patterns/flashing/)
        flash('Bought!')

        return redirect("/")
    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Query data and saves into "rows"
    # https://www.tutorialspoint.com/sqlite/sqlite_group_by.htm for more info
    rows = db.execute("SELECT stock, price, shares, time FROM transactions WHERE username = :username ORDER BY time DESC",
                    username=session["user_id"])

    # Tranform number into $ with 2 decimals
    rows[0]["price"] = usd(rows[0]["price"])

    return render_template("history.html", rows=rows)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    # Search quote
    if request.method == "POST":

        # Ensure symbol was provided
        if not request.form.get("symbol"):
            return apology("Must provide symbol", 400)

        symb = lookup(request.form.get("symbol"))
        
        if symb == None:
            return apology("Symbol does not exist", 400)

        # Format value with usd() function
        symb["price"] = usd(symb["price"])
        
        # Render page passing a dict "symb", explained on helpers.py
        return render_template("quoted.html", symb=symb)

    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Query database for username
        userCheck = db.execute("SELECT * FROM users WHERE username = :username",
                                username=request.form.get("username"))

        # Checks username in DB
        if len(userCheck) == 1:
            return apology("username already exist", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure confirmation wass submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Check passwords are equal
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords didn't match", 400)

        # Hash user's password to store in DB
        hashedPassword = generate_password_hash(request.form.get
                                                ("password"), method='pbkdf2:sha256', salt_length=8)

        # Insert register into DB
        rows = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
                        username=request.form.get("username"),
                        password=hashedPassword)

        flash('Registered!')

        # Redirect user to login page
        return redirect("/")

    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was provided
        if request.form.get("symbol") == "None":
            return apology("Must select symbol", 403)

        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Please input an integer number", 400)

        # Ensure positive number of shares
        if shares < 1:
            return apology("N° of shares is not positive", 400)

        # Query N° of stocks the user owns
        currentStocks = db.execute("SELECT sum(shares) FROM transactions WHERE username = :username AND stock = :stock",
                                username=session["user_id"],
                                stock=request.form.get("symbol"))

        # Check if user has enough stocks to sell
        if shares > int(currentStocks[0]['sum(shares)']):
            return apology("You don't own that many shares", 400)

         # Returns symbol requested
        symb = lookup(request.form.get("symbol"))

        # Saves symbol['price']
        price = symb['price']

        # Query current user's cash
        userCash = db.execute("SELECT cash FROM users WHERE id = :userId",
                                userId=session["user_id"])

        # Storing updated user's cash into newCash
        newCash = userCash[0]["cash"] + float((request.form.get("shares"))) * price

        # UPDATE current user cash in database
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",
                    user_id=session["user_id"],
                    cash=newCash)

        # INSERT row into database
        # 'shares' is stored in negative because sum of all shares (+ and -) show total user shares on /index.html
        rows = db.execute("INSERT INTO transactions (username, stock, price, shares) VALUES (:username, :stock, :price, :shares)",
                            username=session["user_id"],
                            stock=symb['symbol'],
                            price=price,
                            shares=-int(request.form.get("shares")))

        # Pass a message to html. More info at (http://flask.pocoo.org/docs/0.12/patterns/flashing/)
        flash('Sold!')

        # Redirect user to home page
        return redirect("/")

    else:

        # Filters stocks user owns
        # HAVING use (https://stackoverflow.com/a/648089/6389248)
        stocks = db.execute("SELECT stock FROM transactions WHERE username = :username GROUP BY stock HAVING sum(shares) > 0 ORDER BY stock",
                            username=session["user_id"])

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("sell.html", stocks=stocks)


@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    """Restore user's password"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Query database for username
        userCheck = db.execute("SELECT * FROM users WHERE username = :username",
                              username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(userCheck) != 1:
            return apology("invalid username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirmation wass submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        # Check passwords are equal
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords didn't match", 403)

        # Hash user's password to store in DB
        hashedPassword = generate_password_hash(request.form.get
                                                ("password"), method='pbkdf2:sha256', salt_length=8)

        # Insert register into DB
        rows = db.execute("UPDATE users SET hash = :password WHERE username = :username ",
                          username=request.form.get("username"),
                          password=hashedPassword)

        flash('Restored!')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("forgot.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
