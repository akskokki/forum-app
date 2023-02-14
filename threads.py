from db import db
from sqlalchemy.sql import text
import users, messages

def get_list(topic_id):
    sql = text("SELECT T.id, T.title, COUNT(M.id) message_count"\
               " FROM threads T LEFT JOIN messages M ON T.id=M.thread_id"\
               " WHERE topic_id=:topic_id"\
               " GROUP BY T.id"\
               " ORDER BY T.id")
    result = db.session.execute(sql, {"topic_id": topic_id})
    return result.fetchall()

def find_by_id(id):
    sql = text("SELECT T.title, U.username"\
               " FROM threads T, users U"\
               " WHERE T.id=:id AND U.id=T.user_id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()

def create(topic_id, title, content):
    user_id = users.user_id()
    if user_id == 0:
        return 0
    sql = text("INSERT INTO threads (title, topic_id, user_id, time)" \
               " VALUES (:title, :topic_id, :user_id, NOW())"\
               " RETURNING id")
    result = db.session.execute(sql, {
        "title": title,
        "topic_id": topic_id,
        "user_id": user_id   
    })
    [thread_id] = result.fetchone()
    db.session.commit()
    messages.create(thread_id, content)
    return thread_id