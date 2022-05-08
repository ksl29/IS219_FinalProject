import os


class Config(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    BOOTSTRAP_BOOTSWATCH_THEME = 'Simplex'
    DB_DIR = os.getenv('DB_DIR', '../database')
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, '..', DB_DIR, "db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_DIR = os.path.join(BASE_DIR, '../logs')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SESSION_COOKIE_SECURE = False
    DEBUG = True
