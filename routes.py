from app import app
from flask import redirect, render_template, request
from os import getenv
import users, topics, threads, replies

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html", topic_list=topics.get_list())

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("index.html", topic_list=topics.get_list(), notification="Login failed")

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
            return render_template("createuser.html", notification=f"User {username} created successfully")
        else:
            return render_template("createuser.html", notification="User creation failed")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/createtopic", methods=["GET", "POST"])
def createtopic():
    if request.method == "GET":
        return render_template("createtopic.html")
    if request.method == "POST":
        title = request.form["title"]
        topics.create(title)
        return render_template("createtopic.html", notification=f"Topic {title} created successfully")
    
@app.route("/topic/<int:id>")
def topic(id):
    topic = topics.find_by_id(id)
    thread_list = threads.get_list(id)
    return render_template("topic.html", id=id, title=topic[0], threads=thread_list)

@app.route("/topic/<int:topic_id>/createthread", methods=["GET", "POST"])
def createthread(topic_id):
    topic = topics.find_by_id(topic_id)
    if request.method == "GET":
        return render_template("createthread.html", topic_id=topic_id, topic_title=topic[0])
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        thread_id = threads.create(topic_id, title, content)
        if thread_id == 0:
            return render_template("createthread.html", topic_id=topic_id, topic_title=topic[0], notification="Thread creation failed")
        else:
            return redirect(f"/topic/{topic_id}/thread/{thread_id}")

@app.route("/topic/<int:topic_id>/thread/<thread_id>")
def thread(topic_id, thread_id):
    thread = threads.find_by_id(thread_id)
    replies_list = replies.get_list(thread_id)
    return render_template("thread.html", thread_id=thread_id, topic_id=topic_id, thread=thread, replies=replies_list)


@app.route("/topic/<int:topic_id>/thread/<int:thread_id>/createreply", methods=["POST"])
def createreply(topic_id, thread_id):
    content = request.form["content"]
    replies.create(thread_id, content)
    return redirect(f"/topic/{topic_id}/thread/{thread_id}")