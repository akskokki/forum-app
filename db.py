from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

# must uncomment the .replace when deploying to fly.io
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")#.replace("://", "ql://", 1)
db = SQLAlchemy(app)