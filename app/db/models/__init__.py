from datetime import datetime

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import db
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

Base = declarative_base()

task_user = db.Table('task_user', db.Model.metadata,
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'))
                     )


class Task(db.Model, SerializerMixin):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True, unique=False)
    description = db.Column(db.String(300), nullable=True, unique=False)
    due_date = db.Column('due_date', db.Date)
    is_complete = db.Column('is_complete', db.Boolean(), nullable=False, server_default='0')
    is_important = db.Column('is_important', db.Boolean(), nullable=False, server_default='0')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="tasks", uselist=False)

    def __init__(self, title, description, due_date, is_important, is_complete):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.is_important = is_important
        self.is_complete = is_complete


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False, unique=True)
    fname = db.Column(db.String(120), nullable=False, unique=False)
    lname = db.Column(db.String(120), nullable=False, unique=False)
    about = db.Column(db.String(300), nullable=True, unique=False)
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column('registered_on', db.DateTime)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    is_admin = db.Column('is_admin', db.Boolean(), nullable=False, server_default='0')
    tasks = db.relationship("Task",
                            secondary=task_user, backref="users")

    # `roles` and `groups` are reserved words that *must* be defined
    # on the `User` model to use group- or role-based authorization.

    def __init__(self, email, password, fname, lname, is_admin):
        self.email = email
        self.password = password
        self.fname = fname
        self.lname = lname
        self.registered_on = datetime.utcnow()
        self.is_admin = is_admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.email
