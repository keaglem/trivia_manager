"""Extensions module.

Each extension is initialized in the app factory located in app.py
"""
from flask_login import LoginManager
login_manager = LoginManager()

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .settings import DevConfig
engine = create_engine(DevConfig.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()