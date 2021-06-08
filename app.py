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


@app.route("/get_galleries")
def get_galleries():
    galleries = list(mongo.db.galleries.find())
    return render_template("galleries.html", galleries=galleries)


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
            "user_avatar": request.form.get("user_avatar")
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

    if session["user"]:
        return render_template("profile.html", user_name=user_name)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """
    remove session cookie on logout
    """
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_recommendation", methods=["GET", "POST"])
def add_recommendation():
    if request.method == "POST":
        recommendation = {
            "category_name": request.form.get("category_name"),
            "gallery_facilities": request.form.getlist("gallery_facilities"),
            "gallery_name": request.form.get("gallery_name"),
            "gallery_cost": request.form.get("gallery_cost"),
            "gallery_rating": request.form.get("gallery_rating"),
            "gallery_city": request.form.get("gallery_city"),
            "gallery_comments": request.form.get("gallery_comments"),
            "gallery_image": request.form.get("gallery_image"),
            "created_by": session["user"]
        }

        mongo.db.galleries.insert_one(recommendation)
        flash("Recommendation Added - Thank you!")
        return redirect(url_for("get_galleries"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_recommendation.html", categories=categories)


@app.route("/edit_recommendation/<gallery_id>", methods=["GET", "POST"])
def edit_recommendation(gallery_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name"),
            "gallery_facilities": request.form.getlist("gallery_facilities"),
            "gallery_name": request.form.get("gallery_name"),
            "gallery_cost": request.form.get("gallery_cost"),
            "gallery_rating": request.form.get("gallery_rating"),
            "gallery_city": request.form.get("gallery_city"),
            "gallery_comments": request.form.get("gallery_comments"),
            "gallery_image": request.form.get("gallery_image"),
            "created_by": session["user_name"]
        }
        mongo.db.galleries.update({"_id": ObjectId(gallery_id)}, submit)
        flash("Gallery Updated - Thank you!")
    recommendation = mongo.db.galleries.find_one({"_id": ObjectId(gallery_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "edit_recommendation.html", gallery=recommendation,
        categories=categories)


@app.route("/delete_recommendation/<gallery_id>")
def delete_recommendation(gallery_id):
    mongo.db.galleries.remove({"_id": ObjectId(gallery_id)})
    flash("Listing sucessfully Deleted")
    return redirect(url_for("get_galleries"))


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
    flash("Category Successfully deteted")
    return redirect(url_for("get_categories"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)