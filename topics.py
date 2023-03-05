from sqlalchemy.sql import text
from db import db
import users


def get_list():
    sql = text("""
        SELECT O.id, O.title, O.secret, T.id latest_id, T.title latest_title, S.latest_time,
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
            LEFT JOIN SecretTopicUsers STU ON STU.topic_id = O.id AND NOT :user_admin
        WHERE (NOT O.secret OR STU.user_id = :user_id) OR :user_admin
        ORDER BY O.title ASC
    """)
    result = db.session.execute(
        sql, {"user_id": users.user_id(), "user_admin": users.admin()})
    return result.fetchall()


def find_by_id(id):
    sql = text("""
        SELECT O.id, O.title, O.secret
        FROM topics O
            LEFT JOIN SecretTopicUsers STU ON STU.topic_id = O.id AND NOT :user_admin
        WHERE (O.id=:id) AND ((NOT O.secret OR STU.user_id = :user_id) OR :user_admin)
    """)
    result = db.session.execute(
        sql, {"id": id, "user_id": users.user_id(), "user_admin": users.admin()})
    return result.fetchone()


def create(title, secret):
    sql = text("INSERT INTO topics (title, secret) VALUES (:title, :secret)")
    db.session.execute(sql, {"title": title, "secret": secret})
    db.session.commit()


def add_secret_user(topic_id, user_id):
    sql = text("INSERT INTO SecretTopicUsers (topic_id, user_id)"
               " VALUES (:topic_id, :user_id)")
    try:
        db.session.execute(sql, {"topic_id": topic_id, "user_id": user_id})
        db.session.commit()
    except BaseException:
        return False
    return True
