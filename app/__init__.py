from flask import Flask, render_template
from dotenv import load_dotenv

from config import Config
from .extensions import db, login_manager, migrate

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.products import products_bp
    from .routes.admin import admin_bp
    from .routes.cart import cart_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(cart_bp)

    # Charger les models (important pour migrations)
    from . import models  # noqa: F401

    # ✅ cart count disponible dans tous les templates
    from .services.cart_service import cart_count_items

    @app.context_processor
    def inject_cart_count():
        return {"cart_count": cart_count_items()}

    # ✅ page 403 propre
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    return app