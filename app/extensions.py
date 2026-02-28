from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()

# où rediriger si user non connecté
login_manager.login_view = "auth.login"

migrate = Migrate()