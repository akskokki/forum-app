from app import app
from flask import redirect, render_template, request, url_for, session
from os import getenv
import users, topics, threads, messages

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        username = check_args("username")
        notification = check_args("notification")
        return render_template("login.html", notification=notification, username=username)
    if request.method == "POST":
        if users.user_id():
            return redirect("/")
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return redirect(url_for(".login", notification="Invalid username or password", username=username))

@app.route("/createuser", methods=["GET", "POST"])
def createuser():
    if request.method == "GET":
        notification = check_args("notification")
        username = check_args("username")
        return render_template("createuser.html", notification=notification, username=username)
    if request.method == "POST":
        if users.user_id():
            return redirect("/")
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
            return redirect(url_for(".createuser", notification="Username is taken", username=username))

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/createtopic", methods=["GET", "POST"])
def createtopic():
    if not users.admin():
        return redirect("/noperms")
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
    return render_template("topic.html", topic=topic, threads=thread_list)

@app.route("/topic/<int:topic_id>/createthread", methods=["GET", "POST"])
def createthread(topic_id):
    if users.user_id() == 0:
        redirect("/noperms")
    topic = topics.find_by_id(topic_id)
    if request.method == "GET":
        notification = check_args('notification')
        return render_template("createthread.html", topic=topic, notification=notification)
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
    topic = topics.find_by_id(topic_id)
    thread = threads.find_by_id(thread_id)
    messages_list = messages.get_list(thread_id)
    return render_template("thread.html", topic=topic, thread=thread, messages=messages_list)

@app.route("/topic/<int:topic_id>/thread/<int:thread_id>/createmessage", methods=["POST"])
def createmessage(topic_id, thread_id):
    if users.user_id() == 0:
        redirect("/noperms")
    content = request.form["content"]
    messages.create(thread_id, content)
    return redirect(f"/topic/{topic_id}/thread/{thread_id}")

@app.route("/topic/<int:topic_id>/thread/<int:thread_id>/editmessage/<int:message_id>", methods=["POST"])
def editmessage(topic_id, thread_id, message_id):
    new_content = request.form["new_content"]
    if messages.edit(message_id, new_content):
        return redirect(f"/topic/{topic_id}/thread/{thread_id}")
    return redirect("/noperms")

@app.route("/noperms")
def noperms():
    return render_template("noperms.html")