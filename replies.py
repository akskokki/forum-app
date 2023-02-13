from db import db
from sqlalchemy.sql import text
import users

def get_list(thread_id):
    sql = text("SELECT R.id, R.content, U.username"\
               " FROM replies R, users U"\
               " WHERE R.user_id=U.id AND R.thread_id=:thread_id"\
               " ORDER BY R.id")
    result = db.session.execute(sql, {"thread_id": thread_id})
    return result.fetchall()

def create(thread_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO replies (content, thread_id, user_id, time)"\
               " VALUES (:content, :thread_id, :user_id, NOW())")
    db.session.execute(sql, {
        "content": content,
        "thread_id": thread_id,
        "user_id": user_id   
    })
    db.session.commit()
    return True