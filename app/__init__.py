import os
from flask import Flask
from dotenv import load_dotenv

from config import Config
from .extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__)

    # Charge .env depuis la racine du projet
    load_dotenv()

    app.config.from_object(Config)

    # Debug temporaire (tu peux enlever après)
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError(
            "DATABASE_URL is missing. Check your .env file and DATABASE_URL value."
        )

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp
    app.register_blueprint(bp)

    from . import models  # noqa: F401

    return app