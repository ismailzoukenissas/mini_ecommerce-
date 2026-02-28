from flask_login import UserMixin
from bcrypt import hashpw, gensalt, checkpw

from .extensions import db, login_manager

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.LargeBinary, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="client")  # client/admin

    def set_password(self, raw_password: str) -> None:
        self.password_hash = hashpw(raw_password.encode("utf-8"), gensalt())

    def check_password(self, raw_password: str) -> bool:
        return checkpw(raw_password.encode("utf-8"), self.password_hash)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))