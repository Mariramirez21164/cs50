import os
import re
from flask import Flask, jsonify, render_template, request

from cs50 import SQL
from helpers import lookup

# Configure application
app = Flask(__name__)

# Configure for using deprecated JSON return (https://www.reddit.com/r/cs50/comments/7jfz40/pset8_deprecationwarning_requestis_xhr_is/)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Render map"""
    return render_template("index.html")


@app.route("/articles", methods=["GET"])
def articles():
    """Look up articles for geo"""

    # Ensure geo is provided
    if not request.args.get("geo"):
        raise RuntimeError("missing geo")

    # [{'link': 'link', 'title': 'title'}]
    # Pass "geo" variable to lookup for articles and then save into a variable
    articulos = lookup(request.args.get("geo"))

    # I think my job here is really done.
    return jsonify(articulos)


@app.route("/search")
def search():
    """Search for places that match query"""

    # Take postal code from textbox (id=q)
    q = request.args.get("q") + "%"

    # "Delete" commas and split on space bars (Camb,+MA == Camb+MA)

    q = q.replace(',', '').split(' ')

    print(q)
    """
    TODO
    Try to replace commas first, then see what you do with spaces
    What if you count spaces.
    
    Try with some examples on paper first.
    Remember that q0=q[0] + '' + q[1] should not be a reasonable solution just for one case.
    
    Should I divide the queries with another if condition before?
    """
    # search?q=Cambridge
    if len(q) == 1:

        # Make a query on db with "q" and save it to "results"
        results = db.execute("SELECT * FROM places WHERE \
                            postal_code LIKE :q0 OR place_name LIKE :q0 OR admin_name1 LIKE :q0",
                             q0=q[0])

    # search?q=Cambridge,+MA
    elif len(q) == 2:

        results = db.execute("SELECT * FROM places WHERE \
                            place_name LIKE :q0 AND admin_name1 LIKE :q1",
                             q0=q[0], q1=q[1])

    elif len(q) > 2:
        # search?q=Cambrdige,+Massachusetts,+US
        if len(q) == 3:
            print(q)
            results = db.execute("SELECT * FROM places WHERE \
                                place_name LIKE :q0 AND admin_name1 LIKE :q1 AND country_code LIKE :q2",
                                 q0=q[0], q1=q[1], q2=q[2])

        # search?q=New+Haven,+Connecticut,+US
        elif len(q) == 4:
            results = db.execute("SELECT * FROM places WHERE \
                                place_name LIKE :q0 AND admin_name1 LIKE :q1 AND country_code LIKE :q2",
                                 q0=q[0] + " " + q[1], q1=q[2], q2=q[3])

        # search?q=Saint+George+Island,+Alaska,+US
        else:
            results = db.execute("SELECT * FROM places WHERE \
                                place_name LIKE :q0 AND admin_name1 LIKE :q1 AND country_code LIKE :q2",
                                 q0=q[0] + " " + q[1] + " " + q[2], q1=q[3], q2=q[4])

    # Limit results up to 10 articles
    if len(results) > 10:
        results = results[:10]

    return jsonify(results)


@app.route("/update")
def update():
    """Find up to 10 places within view"""

    # Ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # Ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # Explode southwest corner into two variables
    sw_lat, sw_lng = map(float, request.args.get("sw").split(","))

    # Explode northeast corner into two variables
    ne_lat, ne_lng = map(float, request.args.get("ne").split(","))

    # Find 10 cities within view, pseudorandomly chosen if more within view
    if sw_lng <= ne_lng:

        # Doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # Crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # Output places as JSON
    return jsonify(rows)
