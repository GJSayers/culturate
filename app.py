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
@app.route("/get_galleries")
def get_galleries():
    galleries = mongo.db.galleries.find()
    return render_template("galleries.html", galleries=galleries)


@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        """
        checks if user is already a member in the database
        """
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user: 
            flash("Username already exists")
            return redirect(url_for("join"))

        join = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "bio": request.form.get("bio"),
            "profile-pic": request.form.get("profile-pic")
        }  
        mongo.db.users.insert_one(join)

        """
        start a session for the user with a session cookie
        """
        session["user"] = request.form.get("username").lower()
        flash("Thanks for joining the Culturate community!")    
    return render_template("join.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)