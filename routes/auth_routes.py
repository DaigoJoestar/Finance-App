from flask import Blueprint, request, jsonify
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password required"}), 400
    result, error = AuthController.login(data['username'], data['password'])
    if error:
        return jsonify({"error": error}), 401
    return jsonify(result), 200