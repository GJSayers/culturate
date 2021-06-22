import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def get_index():
    return render_template("index.html")


@app.route("/get_listings")
def get_listings():
    listings = list(mongo.db.listings.find())
    return render_template("listings.html", listings=listings)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    listings = list(mongo.db.listings.find({"$text": {"$search": query}}))
    return render_template("listings.html", listings=listings)


@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        """
        checks if user is already a member in the database
        """
        existing_user = mongo.db.users.find_one(
            {"user_name": request.form.get("user_name").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("join"))

        join = {
            "user_name": request.form.get("user_name").lower(),
            "user_email": request.form.get("user_email"),
            "user_password": generate_password_hash(
                request.form.get("user_password")),
            "user_bio": request.form.get("user_bio"),
            "user_avatar": request.form.get("user_avatar"),
            "user_favourites": []
                }
        mongo.db.users.insert_one(join)
        """
        start a session for the user with a session cookie
        """
        session["user"] = request.form.get("user_name").lower()
        flash("Thanks for joining the Culturate community!")
        return redirect(url_for("profile", user_name=session["user"]))

    return render_template("join.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        """
        checks if user is already a member in the database
        """
        existing_user = mongo.db.users.find_one(
            {"user_name": request.form.get("user_name").lower()})

        if existing_user:
            """
            checks password is correct
            """
            if check_password_hash(
                    existing_user["user_password"], request.form.get(
                        "user_password")):
                session["user"] = request.form.get("user_name").lower()
                flash("Hey, {}".format(
                    request.form.get("user_name")))
                return redirect(url_for(
                    "profile", user_name=session["user"]))

            else:
                """
                if password invalid
                """
                flash("Invalid password and / or username")
                return redirect(url_for("login"))
        else:
            """
            if username invalid
            """
            flash("Invalid password and / or username")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<user_name>", methods=["GET", "POST"])
def profile(user_name):
    """
    get session user's username from the database
    """
    user_name = mongo.db.users.find_one(
        {"user_name": session["user"]})["user_name"]
    """
    get session user favourites from the database
    """
    user_favourites = mongo.db.users.find_one(
        {"user_name": session["user"]})["user_favourites"]
    
    favourites_list = []

    for favourite in user_favourites:
        listing = mongo.db.listings.find_one({"_id": favourite})

        favourites_list.append(listing)

        print(type(favourite))
        print("__________________________")
    # listing_id = mongo.db.listings.find_one({"_id": ObjectId})
    # """
    # identify listings that are in user_favourites []
    # """
    # listing = mongo.db.listings.find(
    #     {['listing_id']: {'$in': ["user_favourites"]}})
    # last response not populating cards but cards visible 
    if session["user"]:
        return render_template(
            "profile.html", user_name=user_name,
            user_favourites=favourites_list)
    """
    if user is not in session, re-direct
    """
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """
    remove session cookie on logout
    """
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_listing", methods=["GET", "POST"])
def add_listing():
    if request.method == "POST":
        listing = {
            "category_name": request.form.get("category_name"),
            "listing_facilities": request.form.getlist("listing_facilities"),
            "listing_name": request.form.get("listing_name"),
            "listing_cost": request.form.get("listing_cost"),
            "listing_rating": request.form.get("listing_rating"),
            "listing_city": request.form.get("listing_city"),
            "listing_comments": request.form.get("listing_comments"),
            "listing_image": request.form.get("listing_image"),
            "listing_by": session["user"]
        }

        mongo.db.listings.insert_one(listing)
        flash("listing Added - Thank you!")
        return redirect(url_for("get_listings"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_listing.html", categories=categories)


@app.route("/edit_listing/<listing_id>", methods=["GET", "POST"])
def edit_listing(listing_id):
    if request.method == "POST":

        submit = {
            "category_name": request.form.get("category_name"),
            "listing_facilities": request.form.getlist("listing_facilities"),
            "listing_name": request.form.get("listing_name"),
            "listing_cost": request.form.get("listing_cost"),
            "listing_rating": request.form.get("listing_rating"),
            "listing_city": request.form.get("listing_city"),
            "listing_comments": request.form.get("listing_comments"),
            "listing_image": request.form.get("listing_image"),
            "listing_by": session["user"]
            }
        mongo.db.listings.update({"_id": ObjectId(listing_id)}, submit)
        flash("listing Updated - Thank you!")
    listing = mongo.db.listings.find_one({"_id": ObjectId(listing_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "edit_listing.html", listing=listing,
        categories=categories)    


@app.route("/favourite_listing/<listing_id>", methods=["GET", "POST"])
def favourite_listing(listing_id):
    listing = mongo.db.listings.find_one({"_id": ObjectId(listing_id)})
    print(listing)
    user = mongo.db.users.find_one({"user_name": session["user"]})["_id"]
    print(user)
    user_favourite = listing["_id"]
    print(user_favourite)
    user_name = mongo.db.users.find_one(
        {"user_name": session["user"]})["user_name"]
    print(user_name)
    user_favourites = mongo.db.users.find_one(
        {"user_name": session["user"]})["user_favourites"]
    print(user_favourites)
    if request.method == "POST":
        # check if the listing is already in the
        # user's favourites list in db.
        if user_favourite in user_favourites:
            # remove the listing from the list of favourites
            mongo.db.users.update_one(
                {"_id": user},
                {"$pull": {"user_favourites": listing["_id"]}})
            flash("listing removed from favourites")
            return render_template("listings.html")
        else:
            # add a listing to the session user's
            # favourites section in profile
            mongo.db.users.update_one(
                {"_id": user},
                {"$push": {"user_favourites": listing["_id"]}})
            flash("listing successfully added to favourites")
        return render_template("listings.html")
    return render_template("listings.html")


@app.route("/rate_listing/<listing_id>", methods=["GET", "POST"])
def rate_listing(listing_id):
    listing = mongo.db.listings.find_one({"_id": ObjectId(listing_id)})
    print(listing)
    user = mongo.db.users.find_one({"user_name": session["user"]})["_id"]
    print(user)
    if request.method == "POST":
        listing_rating = {
            "rating_by": session["user"],
            "user_rating": request.form.get("user_rating"),
            "user_comments": request.form.get("user_comments")
            }
        mongo.db.listings.update_one(
            {"_id": ObjectId(listing_id)},
            {"$push": {"listing_rating": listing_rating}}, upsert=True)
        print(listing_rating)
        return render_template("listings.html")
    return render_template("listings.html")


@app.route("/view_ratings/<listing_id>", methods=["GET", "POST"])
def view_ratings(listing_id):
    listing = mongo.db.listings.find_one({"_id": ObjectId(listing_id)})
    print(listing)
    for listing_rating in mongo.db.find_one(
        {"_id": ObjectId(listing_id)})["listing_rating"]:
            print(listing_rating)
    return render_template


@app.route("/delete_listing/<listing_id>")
def delete_listing(listing_id):
    mongo.db.listings.remove({"_id": ObjectId(listing_id)})
    flash("Listing sucessfully Deleted")
    return redirect(url_for("get_listings"))


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.insert_one(category)
        flash("New Category Added, Thank you!")
        return redirect(url_for("get_categories"))

    return render_template("add_category.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
        flash("Category Successfully Updated - Thank you!")
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Category Successfully deleted")
    return redirect(url_for("get_categories"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
