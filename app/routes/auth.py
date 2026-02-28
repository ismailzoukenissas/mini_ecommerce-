from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from ..extensions import db
from ..models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/register")
def register_form():
    return render_template("auth/register.html")

@auth_bp.post("/register")
def register_submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    # Validations simples (serveur)
    if not name or not email or not password:
        flash("Tous les champs sont obligatoires.")
        return redirect(url_for("auth.register_form"))

    # Email unique
    if User.query.filter_by(email=email).first():
        flash("Cet email est déjà utilisé.")
        return redirect(url_for("auth.register_form"))

    user = User(name=name, email=email, role="client")
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    flash("Compte créé ✅ يمكنك الآن تسجيل الدخول.")
    return redirect(url_for("auth.login_form"))

@auth_bp.get("/login")
def login_form():
    return render_template("auth/login.html")

@auth_bp.post("/login")
def login_submit():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    user = User.query.filter_by(email=email).first()

    # ⚠️ Erreur générique (ne pas préciser email ou password)
    if (not user) or (not user.check_password(password)):
        flash("Identifiants invalides.")
        return redirect(url_for("auth.login_form"))

    login_user(user)
    flash("Connexion réussie ✅")
    return redirect(url_for("main.profile"))

@auth_bp.post("/logout")
def logout():
    logout_user()
    flash("Déconnecté ✅")
    return redirect(url_for("main.home"))