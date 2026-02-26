from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .extensions import db
from .models import User

bp = Blueprint("main", __name__)

@bp.get("/")
def home():
    return "Mini Shop OK ✅"

# Créer un user (juste pour test)
@bp.post("/seed-user")
def seed_user():
    data = request.get_json(force=True)
    name = data.get("name", "Test User")
    email = data["email"]
    password = data["password"]

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already used"}), 400

    u = User(name=name, email=email)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return jsonify({"message": "User created", "id": u.id})

@bp.post("/login")
def login():
    data = request.get_json(force=True)
    email = data["email"]
    password = data["password"]

    u = User.query.filter_by(email=email).first()
    # message générique (bonne pratique)
    if not u or not u.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    login_user(u)
    return jsonify({"message": "Logged in", "user_id": u.id})

@bp.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})

@bp.get("/me")
@login_required
def me():
    return jsonify({"id": current_user.id, "email": current_user.email, "role": current_user.role})