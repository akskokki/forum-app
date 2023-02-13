from app import app
from flask import redirect, render_template, request, url_for
from os import getenv
import users, topics, threads, replies

app.secret_key = getenv("SECRET_KEY")

def check_args(arg):
    if arg in request.args:
        return request.args[arg]
    return None

@app.route("/")
def index():
    notification = check_args("notification")
    username = check_args("username")
    return render_template("index.html", topic_list=topics.get_list(), notification=notification, username=username)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return redirect(url_for(".index", notification="Invalid username or password", username=username))

@app.route("/createuser", methods=["GET", "POST"])
def createuser():
    if request.method == "GET":
        notification = check_args("notification")
        username = check_args("username")
        return render_template("createuser.html", notification=notification, username=username)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_retype = request.form["password_retype"]
        if len(username) < 1 or len(password) < 1:
            return redirect(url_for(".createuser", notification="Username and password must not be blank", username=username))
        if password != password_retype:
            return redirect(url_for(".createuser", notification="Passwords don't match", username=username))
        if users.create(username, password):
            users.login(username, password)
            return redirect(url_for(".index", notification="User created successfully"))
        else:
            return redirect(url_for(".createuser.html", notification="Username is taken", username=username))

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
        return redirect("/")
    
@app.route("/topic/<int:id>")
def topic(id):
    topic = topics.find_by_id(id)
    thread_list = threads.get_list(id)
    return render_template("topic.html", id=id, title=topic[0], threads=thread_list)

@app.route("/topic/<int:topic_id>/createthread", methods=["GET", "POST"])
def createthread(topic_id):
    topic = topics.find_by_id(topic_id)
    if request.method == "GET":
        notification = check_args('notification')
        return render_template("createthread.html", topic_id=topic_id, topic_title=topic[0], notification=notification)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        thread_id = threads.create(topic_id, title, content)
        if thread_id == 0:
            return redirect("/noperms")
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

@app.route("/noperms")
def noperms():
    return render_template("noperms.html")