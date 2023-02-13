from db import db
from sqlalchemy.sql import text
import users

def get_list(topic_id):
    sql = text("SELECT id, title FROM threads WHERE topic_id=:topic_id ORDER BY id")
    result = db.session.execute(sql, {"topic_id": topic_id})
    return result.fetchall()

def find_by_id(id):
    sql = text("SELECT T.title, T.content, U.username"\
               " FROM threads T, users U"\
               " WHERE T.id=:id AND U.id=T.user_id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()

def create(topic_id, title, content):
    user_id = users.user_id()
    if user_id == 0:
        return 0
    sql = text("INSERT INTO threads (title, content, topic_id, user_id, time)" \
               " VALUES (:title, :content, :topic_id, :user_id, NOW())"\
               " RETURNING id")
    result = db.session.execute(sql, {
        "title": title,
        "content": content,
        "topic_id": topic_id,
        "user_id": user_id   
    })
    [thread_id] = result.fetchone()
    db.session.commit()
    return thread_id