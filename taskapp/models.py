import datetime
import os

import itsdangerous
from flask import current_app
try:
    from flask_login import UserMixin
except:
    from flask.ext.login import UserMixin
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from .extensions import Base
import sqlalchemy as db



class User(Base, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean(), default=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, plaintext_pass):
        self.name = name
        self.email = email
        self.set_password(plaintext_pass)

    def set_password(self, plaintext_pass):
        self.password = generate_password_hash(plaintext_pass)

    def verify_password(self, plaintext_pass):
        return check_password_hash(self.password, plaintext_pass)

    def __repr__(self):
        return "<User '%s'>" % self.name

    def __str__(self):
        return self.name

    @classmethod
    def from_email(cls, email):
        """Return a user object for a given email."""
        return cls.query.filter(User.email == email).first()

    @classmethod
    def from_name_or_email(cls, name_or_email):
        """Return a user object for a given username or email."""
        return cls.query.filter(or_(User.name == name_or_email, User.email == name_or_email)).first()

    @classmethod
    def authenticate(cls, name_or_email, plaintext_pass):
        """Return a User object given valid credentials.

        The login parameter may be either the username or password.
        None is returned on failure.
        """
        user = cls.from_name_or_email(name_or_email)
        if user and user.verify_password(plaintext_pass):
            return user
        return None

    def get_token(self, tag):
        """Return a token that can be used to validate or reset a user.

        The tag is a plain string that is used as a namespace. It must also be
        passed to from_token."""
        serialzer = itsdangerous.URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serialzer.dumps(self.id, salt=tag)

    @classmethod
    def from_token(cls, token, tag, max_age=None):
        """Given a token, return the user for that token."""
        serialzer = itsdangerous.URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            id = serialzer.loads(token, max_age=max_age, salt=tag)
        except itsdangerous.BadData:
            return None
        return cls.query.get(int(id))


class Game(Base):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=False)
    current_question_id = db.Column(db.ForeignKey('question.id'))
    current_question = db.orm.relationship('Question',
                                           foreign_keys=[current_question_id])

    def is_active(self):
        return self.active

class Question(Base):
    """
    Database for an individual run of the simulation
    """
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    question_number = db.Column(db.Integer)
    game_id = db.Column(db.ForeignKey('game.id'))

    game = db.orm.relationship(
        'Game',
        primaryjoin='Question.game_id == Game.id',
        backref=db.orm.backref('questions', lazy='dynamic', collection_class=list)
    )

    _serialize_field = ['id'
                        ]

    def serialize(self):

        return_dict = {field_name: getattr(self, field_name) for field_name in self._serialize_field }
        return_dict['question'] = self.submission.serialize()
        return return_dict








class Answer(Base):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.ForeignKey('question.id'))
    user_id = db.Column(db.ForeignKey('user.id'))
    answer = db.String(256)

    user = db.orm.relationship(
        'User',
        backref=db.orm.backref('answers', lazy='dynamic', collection_class=list)
    )

    question = db.orm.relationship(
        'Question',
        backref=db.orm.backref('answers', lazy='dynamic', collection_class=list)
    )

class Prompt(Base):
    """
    Database for an individual run of the simulation
    """
    __tablename__ = 'prompt'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    prompt = db.Column(db.String(256), nullable=False)
    answer = db.Column(db.String(256), nullable=False)

    question = db.orm.relationship(
        'Question',
        backref=db.orm.backref('prompts', lazy='dynamic', collection_class=list)
    )