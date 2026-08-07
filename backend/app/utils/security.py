import bcrypt
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def hash_password(password: str) -> str:
    """Hash a password with bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def role_required(*roles):
    """
    Decorator to enforce Role-Based Access Control (RBAC).
    Requires a valid JWT and checks if the user's role matches any of the allowed roles.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') not in roles:
                return jsonify({"msg": "Forbidden: Insufficient privileges", "role_required": roles}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def admin_required():
    return role_required('admin')

def hospital_required():
    return role_required('hospital', 'admin')  # Admins can sometimes act on behalf of hospitals

def donor_required():
    return role_required('donor')
