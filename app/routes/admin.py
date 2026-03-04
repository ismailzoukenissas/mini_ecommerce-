from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..decorators import admin_required
from ..extensions import db
from ..models import Product

admin_bp = Blueprint("admin", __name__)

@admin_bp.get("/admin/products/new")
@admin_required
def product_new_form():
    return render_template("admin/product_new.html")

@admin_bp.post("/admin/products/new")
@admin_required
def product_new_submit():
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    price = request.form.get("price", "").strip()
    stock = request.form.get("stock", "").strip()

    if not name or not price:
        flash("Nom et prix sont obligatoires.")
        return redirect(url_for("admin.product_new_form"))

    try:
        price_val = float(price)
        stock_val = int(stock) if stock else 0
    except ValueError:
        flash("Prix ou stock invalide.")
        return redirect(url_for("admin.product_new_form"))

    p = Product(
        name=name,
        description=description,
        price=price_val,
        stock=stock_val,
        is_active=True
    )
    db.session.add(p)
    db.session.commit()

    flash("Produit ajouté ✅")
    return redirect(url_for("products.products_index"))