from functools import wraps
from flask import abort
from flask_login import current_user, login_required

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped(*args, **kwargs):
        if getattr(current_user, "role", None) != "admin":
            abort(403)
        return view_func(*args, **kwargs)
    return wrapped