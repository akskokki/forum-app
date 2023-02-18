from db import db
from sqlalchemy.sql import text
import users, messages

def get_list(topic_id):
    sql = text("""
        SELECT T.id, T.title, TU.username, S.latest_time, MU.username latest_user, S.message_count
        FROM threads T
            LEFT JOIN (
                SELECT thread_id, MAX(time) latest_time, COUNT(id) message_count
                FROM messages
                GROUP BY thread_id
            ) S ON T.id = S.thread_id
            LEFT JOIN messages M ON M.thread_id = T.id
                AND M.time = S.latest_time
            LEFT JOIN users TU ON T.user_id = TU.id
            LEFT JOIN users MU ON M.user_id = MU.id
        WHERE T.topic_id = :topic_id
        ORDER BY M.time DESC
    """)
    result = db.session.execute(sql, {"topic_id": topic_id})
    return result.fetchall()

def find_by_id(id):
    sql = text("SELECT T.id, T.title, U.username"\
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

def edit(thread_id, new_title):
    user_id = users.user_id()
    sql = text("UPDATE threads SET title=:new_title WHERE user_id=:user_id AND id=:thread_id RETURNING id")
    result = db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id, "new_title": new_title})
    db.session.commit()
    return len(result.fetchone())

def remove(thread_id):
    user_id = users.user_id()
    sql = text("DELETE FROM threads CASCADE WHERE user_id=:user_id AND id=:thread_id")
    db.session.execute(sql, {"user_id": user_id, "thread_id": thread_id})
    db.session.commit()