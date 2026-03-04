from __future__ import annotations
from flask import session

CART_KEY = "cart"  # {"1": 2, "5": 1} -> product_id(str) : qty(int)

def get_cart() -> dict[str, int]:
    cart = session.get(CART_KEY)
    if not isinstance(cart, dict):
        cart = {}
        session[CART_KEY] = cart
    return cart

def cart_count_items() -> int:
    cart = get_cart()
    return sum(int(q) for q in cart.values())

def add_to_cart(product_id: int, qty: int = 1) -> None:
    cart = get_cart()
    pid = str(product_id)
    current = int(cart.get(pid, 0))
    cart[pid] = max(1, current + int(qty))
    session.modified = True

def remove_from_cart(product_id: int) -> None:
    cart = get_cart()
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
        session.modified = True

def set_qty(product_id: int, qty: int) -> None:
    cart = get_cart()
    pid = str(product_id)
    qty = int(qty)
    if qty <= 0:
        cart.pop(pid, None)
    else:
        cart[pid] = qty
    session.modified = True

def clear_cart() -> None:
    session[CART_KEY] = {}
    session.modified = True