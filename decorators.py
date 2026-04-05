from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def role_required(*allowed_roles):
    """
    Decorator: @role_required('admin', 'analyst')
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            username = get_jwt_identity()
            from models import User
            user = User.query.filter_by(username=username).first()
            if not user or not user.active:
                return jsonify({"error": "User inactive or not found"}), 403
            g.current_user = user
            
            # Check if user's role is in allowed_roles
            if user.role not in allowed_roles:
                return jsonify({"error": "Insufficient permissions"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
