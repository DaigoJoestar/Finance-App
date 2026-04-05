from flask import Blueprint, request, jsonify
from decorators import role_required
from controllers.user_controller import UserController

user_bp = Blueprint('users', __name__)

@user_bp.route('', methods=['POST'])
@role_required('admin')
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data"}), 400
    result, error, status = UserController.create_user(data)
    if error:
        return jsonify(error), status
    return jsonify(result), status

@user_bp.route('', methods=['GET'])
@role_required('admin')
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    result, status = UserController.get_users(page, per_page)
    return jsonify(result), status

@user_bp.route('/<int:user_id>', methods=['GET'])
@role_required('admin')
def get_user(user_id):
    result, error, status = UserController.get_user(user_id)
    if error:
        return jsonify(error), status
    return jsonify(result), status

@user_bp.route('/<int:user_id>', methods=['PUT'])
@role_required('admin')
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data"}), 400
    result, error, status = UserController.update_user(user_id, data)
    if error:
        return jsonify(error), status
    return jsonify(result), status

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@role_required('admin')
def delete_user(user_id):
    result, error, status = UserController.delete_user(user_id)
    if error:
        return jsonify(error), status
    return jsonify(result), status