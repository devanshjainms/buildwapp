import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

# global database object
# (initialized without app and later bound in create_app)
db = SQLAlchemy()


def create_app(test_config=None):
    """Application factory."""
    load_dotenv()
    app = Flask(__name__)
    database_url = os.getenv("DATABASE_URL", "sqlite:///app.db")
    app.config.update(
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    CORS(app)

    with app.app_context():
        from . import models  # noqa: F401
        db.create_all()
        from .routes import bp
        app.register_blueprint(bp)

    return app

