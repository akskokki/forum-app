import secrets
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from os import getenv

def create(username, password):
    try:
        sql = text("INSERT INTO users (username, password, admin)"\
                   " VALUES (:username, :password, :admin)")
        db.session.execute(sql, {
            "username": username, 
            "password": generate_password_hash(password), 
            "admin": username == getenv("ADMIN_USERNAME")
        })
        db.session.commit()
    except:
        return False
    return True

def login(username, password):
    sql = text("SELECT id, password, admin FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["admin"] = user.admin
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def logout():
    session.clear()

def user_id():
    return session.get("user_id", 0)

def admin():
    return session.get("admin", False)