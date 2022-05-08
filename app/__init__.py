"""A simple flask web app"""
import os

from flask import Flask
from flask_bootstrap import Bootstrap5

from app.auth import auth
from app.cli import create_database
from app.db import db, database
from app.db.models import User
from app.error_handlers import error_handlers


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.secret_key = 'This is an INSECURE secret!! DO NOT use this in production!!'
    # added bootstrap 5 to project
    bootstrap = Bootstrap5(app);
    # these load functions with web interface
    app.register_blueprint(database)
    app.register_blueprint(auth)
    # these load functionality without a web interface
    app.register_blueprint(error_handlers)
    db_dir = "../database/db.sqlite"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath(db_dir)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    # add command function to cli commands
    app.cli.add_command(create_database)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app
