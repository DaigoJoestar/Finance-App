from flask import Blueprint, request, jsonify, g
from decorators import role_required
from controllers.record_controller import RecordController

record_bp = Blueprint('records', __name__)

@record_bp.route('', methods=['POST'])
@role_required('admin')
def create_record():
    data = request.get_json()
    user_id = data.get("user_id", g.current_user.id )
    if not data:
        return jsonify({"error": "No input data"}), 400
    result, error, status = RecordController.create_record(data, user_id )
    if error:
        return jsonify(error), status
    return jsonify(result), status

@record_bp.route('', methods=['GET'])
@role_required('viewer')
def get_records():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    filters = {
        'type': request.args.get('type'),
        'category': request.args.get('category'),
        'date_from': request.args.get('date_from'),
        'date_to': request.args.get('date_to')
    }
    result, status = RecordController.get_records(filters, page, per_page)
    return jsonify(result), status

@record_bp.route('/<int:record_id>', methods=['GET'])
@role_required('viewer')
def get_record(record_id):
    result, error, status = RecordController.get_record(record_id)
    if error:
        return jsonify(error), status
    return jsonify(result), status

@record_bp.route('/<int:record_id>', methods=['PUT'])
@role_required('admin')
def update_record(record_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data"}), 400
    result, error, status = RecordController.update_record(record_id, data)
    if error:
        return jsonify(error), status
    return jsonify(result), status

@record_bp.route('/<int:record_id>', methods=['DELETE'])
@role_required('admin')
def delete_record(record_id):
    result, error, status = RecordController.delete_record(record_id)
    if error:
        return jsonify(error), status
    return jsonify(result), status