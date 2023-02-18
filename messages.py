from db import db
from sqlalchemy.sql import text
import users

def get_list(thread_id):
    sql = text("SELECT M.id, M.content, U.username, M.time"\
               " FROM messages M, users U"\
               " WHERE M.user_id=U.id AND M.thread_id=:thread_id"\
               " ORDER BY M.id")
    result = db.session.execute(sql, {"thread_id": thread_id})
    return result.fetchall()

def create(thread_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO messages (content, thread_id, user_id, time)"\
               " VALUES (:content, :thread_id, :user_id, NOW())")
    db.session.execute(sql, {
        "content": content,
        "thread_id": thread_id,
        "user_id": user_id   
    })
    db.session.commit()
    return True

def edit(message_id, new_content):
    user_id = users.user_id()
    sql = text("UPDATE messages SET content=:new_content WHERE user_id=:user_id AND id=:message_id RETURNING id")
    result = db.session.execute(sql, {"message_id": message_id, "user_id": user_id, "new_content": new_content})
    db.session.commit()
    return len(result.fetchone())