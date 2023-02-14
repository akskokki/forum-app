from db import db
from sqlalchemy.sql import text

def get_list():
    sql = text("""
        SELECT O.id, O.title, T.id latest_id, T.title latest_title, S.latest_time,
            U.username latest_user, S.message_count, S.thread_count
        FROM topics O
            LEFT JOIN (
                SELECT T.topic_id, MAX(M.time) latest_time,
                    COUNT(M.id) message_count, COUNT(DISTINCT T.id) thread_count
                FROM messages M
                    JOIN threads T ON M.thread_id = T.id
                GROUP BY T.topic_id
            ) S ON O.id = S.topic_id
            LEFT JOIN messages M ON M.time = S.latest_time
            LEFT JOIN threads T ON T.id = M.thread_id
            LEFT JOIN users U ON U.id = M.user_id
        ORDER BY O.title ASC
    """)

    sql2 = text("SELECT O.id, O.title, COUNT(DISTINCT H.id) thread_count, COUNT(M.id) message_count "\
                "FROM topics O "\
                "LEFT JOIN threads H ON O.id=H.topic_id "\
                "LEFT JOIN messages M ON H.id=M.thread_id "\
                "GROUP BY O.id "\
                "ORDER BY O.id")
    result = db.session.execute(sql)
    return result.fetchall()

def find_by_id(id):
    sql = text("SELECT title FROM topics WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()

def create(title):
    sql = text("INSERT INTO topics (title) VALUES (:title)")
    db.session.execute(sql, {"title": title})
    db.session.commit()