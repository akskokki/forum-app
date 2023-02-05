from app import app
from flask import redirect, render_template, request
from os import getenv
import users

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("index.html", notification="Login failed")

@app.route("/createuser", methods=["GET", "POST"])
def createuser():
    if request.method == "GET":
        return render_template("createuser.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_retype = request.form["password_retype"]
        if password != password_retype:
            return render_template("createuser.html", notification="Passwords don't match")
        if users.create(username, password):
            return render_template("createuser.html", notification=f"User <b>{username}</b> created successfully")
        else:
            return render_template("createuser.html", notification="User creation failed")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")