from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..models import Product
from ..services.cart_service import get_cart, add_to_cart, remove_from_cart, set_qty

cart_bp = Blueprint("cart", __name__)

@cart_bp.get("/cart")
def cart_view():
    cart = get_cart()  # dict[str,int]
    items = []
    total = 0.0

    # Charger les produits du panier depuis la DB
    product_ids = [int(pid) for pid in cart.keys()] if cart else []
    products = Product.query.filter(Product.id.in_(product_ids)).all() if product_ids else []
    products_map = {p.id: p for p in products}

    for pid_str, qty in cart.items():
        pid = int(pid_str)
        p = products_map.get(pid)
        if not p:
            continue
        line_total = float(p.price) * int(qty)
        total += line_total
        items.append({"product": p, "qty": int(qty), "line_total": line_total})

    return render_template("cart/cart.html", items=items, total=total)

@cart_bp.post("/cart/add/<int:product_id>")
def cart_add(product_id):
    # Optionnel: qty depuis form, sinon 1
    qty = request.form.get("qty", "1")
    try:
        qty = int(qty)
    except ValueError:
        qty = 1

    p = Product.query.get_or_404(product_id)

    if not p.is_active:
        flash("Produit indisponible.")
        return redirect(url_for("products.products_index"))

    add_to_cart(product_id, qty)
    flash("Ajouté au panier ✅")
    return redirect(request.referrer or url_for("products.products_index"))

@cart_bp.post("/cart/remove/<int:product_id>")
def cart_remove(product_id):
    remove_from_cart(product_id)
    flash("Supprimé du panier ✅")
    return redirect(url_for("cart.cart_view"))

@cart_bp.post("/cart/update/<int:product_id>")
def cart_update(product_id):
    qty = request.form.get("qty", "1")
    try:
        qty = int(qty)
    except ValueError:
        qty = 1
    set_qty(product_id, qty)
    flash("Panier mis à jour ✅")
    return redirect(url_for("cart.cart_view"))