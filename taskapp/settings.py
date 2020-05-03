import os


class Config(object):
    SECRET_KEY = os.environ.get('CONTESTAPP_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    MAX_CONTENT_LENGTH = 65535 # 16 KiB, maximum size of MySQL TEXT field
    # SERVER_NAME = 'localhost' # TODO: Change me to server name
    MAIL_DEFAULT_SENDER = 'admin@contest.com' # TODO: change me
    MAIL_SUPPRESS_SEND = False # Set to true if you don't want to use emails
    MAX_ENTRIES_PER_PAGE = 10


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/task'


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    BOOTSTRAP_SERVE_LOCAL = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/tasks'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:////home/keaglem/database/tasks.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True