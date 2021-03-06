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


# to display all listings
@app.route("/get_listings")
def get_listings():
    listings = list(mongo.db.listings.find())
    return render_template(
        "listings.html", listings=listings)


# to display one listing
@app.route("/listing_page/<listing_id>")
def listing_page(listing_id):
    listing = mongo.db.listings.find_one({"_id": ObjectId(listing_id)})
    return render_template(
        "listing_page.html", listing=listing)


# for searching the listings
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    listings = list(mongo.db.listings.find({"$text": {"$search": query}}))
    return render_template("listings.html", listings=listings)


# route to join / sign-up for the site
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


# route to edit a user profile
@app.route("/edit_user/<user>", methods=["GET", "POST"])
def edit_user(user):
    if request.method == "POST":
        update_details = {"$set": {
            "user_name": request.form.get("user_name").lower(),
            "user_email": request.form.get("user_email"),
            "user_bio": request.form.get("user_bio")
        }}
        mongo.db.users.update_one(
            {"_id": ObjectId(user)}, update_details, upsert=True)
        flash("Thanks for keeping your details up to date!")
    user = mongo.db.users.find_one(
        {"_id": ObjectId(user)})
    user_name = mongo.db.users.find_one(
        {"user_name": session["user"]})["user_name"]
    return render_template("edit_user.html",
                           user=user, user_name=user_name)


# route to login
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


# route to populate profile page
@app.route("/profile/<user_name>", methods=["GET", "POST"])
def profile(user_name):
    users = list(mongo.db.users.find())
    categories = mongo.db.categories.find().sort("category_name", 1)
    listing = list(mongo.db.listings.find())
    """
    get session user's username from the database
    """
    user_name = mongo.db.users.find_one(
        {"user_name": session["user"]})["user_name"]
    """
    get session user's profile from the database
    """
    user = mongo.db.users.find_one(
        {"user_name": session["user"]})
    """
    get session user favourites from the database
    """
    user_favourites = mongo.db.users.find_one(
        {"user_name": session["user"]})["user_favourites"]

    favourites_list = []
    """
    iterate through listings to find favourites in listings
    """
    for favourite in user_favourites:
        listing = mongo.db.listings.find_one({"_id": favourite})

        favourites_list.append(listing)
    if session["user"]:
        return render_template(
            "profile.html", user_name=user_name,
            user_favourites=favourites_list, user=user,
            categories=categories, users=users)
    """
    if user is not in session, re-direct
    """
    return redirect(url_for("login"))


# route to delete a user
@app.route("/delete_user/<user>")
def delete_user(user):
    mongo.db.users.remove({"_id": ObjectId(user)})
    flash("User profile successfully deleted")
    return redirect(url_for("get_listings"))


# route to delete a user from admin profile directly
@app.route("/delete_entry/<entry>")
def delete_entry(entry):
    mongo.db.users.remove({"_id": ObjectId(entry)})
    flash("User profile successfully deleted")
    return redirect(url_for("get_listings"))


# route to add a logout
@app.route("/logout")
def logout():
    """
    remove session cookie on logout
    """
    session.pop("user")
    return redirect(url_for("login"))


# route to add a listing
@app.route("/add_listing", methods=["GET", "POST"])
def add_listing():
    if request.method == "POST":

        listing = {
            "category_name": request.form.get("category_name"),
            "listing_facilities": request.form.getlist("listing_facilities"),
            "listing_name": request.form.get("listing_name"),
            "listing_cost": request.form.get("listing_cost"),
            "listing_rating": [],
            "listing_city": request.form.get("listing_city"),
            "listing_image": request.form.get("listing_image"),
            "listing_by": session["user"],
            "listing_website": request.form.get("listing_website"),
            "listing_avg_rating": "",
            "listing_comments": request.form.get("listing_comments"),
            "listing_location": request.form.get("listing_location")
        }

        mongo.db.listings.insert_one(listing)
        flash("listing Added - Thank you!")
        return redirect(url_for("get_listings"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_listing.html", categories=categories)


# route to edit a listing
@app.route("/edit_listing/<listing_id>", methods=["GET", "POST"])
def edit_listing(listing_id):
    if request.method == "POST":

        submit = {
            "category_name": request.form.get("category_name"),
            "listing_facilities": request.form.getlist("listing_facilities"),
            "listing_name": request.form.get("listing_name"),
            "listing_cost": request.form.get("listing_cost"),
            "listing_city": request.form.get("listing_city"),
            "listing_image": request.form.get("listing_image"),
            "listing_by": session["user"],
            "listing_website": request.form.get("listing_website"),
            "listing_comments": request.form.get("listing_comments"),
            "listing_location": request.form.get("listing_location")
        }

        mongo.db.listings.update({"_id": ObjectId(listing_id)}, submit)
        flash("listing Updated - Thank you!")
    listing = mongo.db.listings.find_one({"_id": ObjectId(listing_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "edit_listing.html", listing=listing,
        categories=categories)


# route to save listing as favourite
@app.route("/favourite_listing/<listing_id>", methods=["GET", "POST"])
def favourite_listing(listing_id):
    listing = mongo.db.listings.find_one({"_id": ObjectId(listing_id)})
    user = mongo.db.users.find_one({"user_name": session["user"]})["_id"]
    user_favourite = listing["_id"]
    user_favourites = mongo.db.users.find_one(
        {"user_name": session["user"]})["user_favourites"]

    if request.method == "POST":
        # check if the listing is already in the
        # user's favourites list in db.
        if user_favourite in user_favourites:
            # remove the listing from the list of favourites
            mongo.db.users.update_one(
                {"_id": user},
                {"$pull": {"user_favourites": listing["_id"]}})
            flash("listing removed from favourites")
            return redirect(url_for("get_listings"))
        else:
            # add a listing to the session user's
            # favourites section in profile
            mongo.db.users.update_one(
                {"_id": user},
                {"$push": {"user_favourites": listing["_id"]}})
            flash("listing successfully added to favourites")
            return redirect(url_for("get_listings"))
    return render_template("listings.html")


# route to rate listing with star radio buttons
@app.route("/rate_listing/<listing_id>", methods=["GET", "POST"])
def rate_listing(listing_id):
    listing = mongo.db.listings.find_one({"_id": ObjectId(listing_id)})
    user = mongo.db.users.find_one({"user_name": session["user"]})["_id"]
    author = mongo.db.listings.find_one({"rating_by": user})

    if session["user"] and author != user:
        if request.method == "POST":
            listing_rating = {
                "rating_by": session["user"],
                "user_rating": request.form.get("user_rating"),
                "user_comments": request.form.get("user_comments")
            }
            mongo.db.listings.update_one({"_id": ObjectId(listing_id)},
                                         {"$push": {"listing_rating":
                                          listing_rating}})
            return redirect(url_for(
                "get_listings", listing=listing, user=user))
        """
        if user is not in session, re-direct
        """
        return redirect(url_for("login"))
    flash("you have already rated this listing")
    return redirect(url_for("listing_page", listing_id=listing_id))


# route to delete a listing
@app.route("/delete_listing/<listing_id>")
def delete_listing(listing_id):
    mongo.db.listings.remove({"_id": ObjectId(listing_id)})
    flash("Listing sucessfully Deleted")
    return redirect(url_for("get_listings"))


# route to get list of categories
# available to superuser
@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


# route to add new categories
# available to superuser
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


# route to edit categories
# available to superuser
@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {"$set": {
            "category_name": request.form.get("category_name")
        }}
        mongo.db.categories.update_one(
            {"_id": ObjectId(category_id)}, submit, upsert=True)
        flash("Category Successfully Updated - Thank you!")
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


# route to delete categories
# available to superuser
@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Category Successfully deleted")
    return redirect(url_for("get_categories"))


# error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)


@app.errorhandler(500)
def internal(error):
    return render_template("500.html", error=error)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
