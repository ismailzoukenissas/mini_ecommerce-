from flask import Blueprint, render_template
from flask_login import login_required
from ..decorators import admin_required

main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def home():
    return render_template("layouts/base.html")  # simple test, ou crée home.html si tu veux

@main_bp.get("/profile")
@login_required
def profile():
    return render_template("profile.html")

@main_bp.get("/admin-test")
@admin_required
def admin_test():
    return render_template("admin_test.html")