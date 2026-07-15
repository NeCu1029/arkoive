# 잡다한 것들 저장

from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

bc = Bcrypt()
db = SQLAlchemy()
manager = LoginManager()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
