"""A simple flask web app"""
import os

from flask import Flask
from flask_bootstrap import Bootstrap5

from app.auth import auth
from app.cli import create_database
from app.db import db, database
from app.db.models import User
from app.error_handlers import error_handlers
from app.logging_config import log_con, LOGGING_CONFIG
from app.simple_pages import simple_pages


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif os.environ.get("FLASK_ENV") == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object("app.config.TestingConfig")

    # added bootstrap 5 to project
    bootstrap = Bootstrap5(app);
    # these load functions with web interface
    app.register_blueprint(database)
    app.register_blueprint(auth)
    app.register_blueprint(simple_pages)
    # these load functionality without a web interface
    app.register_blueprint(error_handlers)
    app.register_blueprint(log_con)
    # add command function to cli commands
    app.cli.add_command(create_database)
    # add command function to cli commands
    db.init_app(app)
    app.cli.add_command(create_database)


    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app
