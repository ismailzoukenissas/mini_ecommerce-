from flask import Blueprint, render_template
from ..models import Product

products_bp = Blueprint("products", __name__)

@products_bp.get("/products")
def products_index():
    products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).all()
    return render_template("products/index.html", products=products)

@products_bp.get("/products/<int:product_id>")
def products_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("products/detail.html", product=product)