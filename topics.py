from db import db
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT O.id, O.title, COUNT(H.id) thread_count "\
               "FROM topics O LEFT JOIN threads H ON O.id=H.topic_id "\
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