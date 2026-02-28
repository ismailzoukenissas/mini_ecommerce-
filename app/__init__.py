from flask import Flask
from dotenv import load_dotenv

from config import Config
from .extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Charger les models (important pour migrations)
    from . import models  # noqa: F401
    from flask import render_template

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403
    return app