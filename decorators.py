from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            username = get_jwt_identity()
            
            from models import User 
            user = User.query.filter_by(username=username).first()


            if not user or not user.active: # Check your model field name (active vs is_active)
                return jsonify({"msg": "User account is disabled or not found"}), 403
            
            # Store user in flask.g for use in the actual view function
            g.current_user = user


            # Allow Admins by default OR check if user's role is in the list
            if user.role != 'admin' and user.role not in allowed_roles:
                return jsonify({"msg": f"Role '{user.role}' does not have access"}), 403
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator