from flask import Blueprint, request, jsonify
from decorators import role_required
from controllers.dashboard_controller import DashboardController

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/summary', methods=['GET'])
@role_required('analyst', 'viewer')
def summary():
    year = request.args.get('year', type=int)
    result, status = DashboardController.get_summary(year)
    return jsonify(result), status

@dashboard_bp.route('/by-category', methods=['GET'])
@role_required('analyst', 'viewer')
def category_totals():
    year = request.args.get('year', type=int)
    result, status = DashboardController.get_category_totals(year)
    return jsonify(result), status

@dashboard_bp.route('/recent', methods=['GET'])
@role_required('analyst', 'viewer')
def recent():
    limit = request.args.get('limit', 5, type=int)
    result, status = DashboardController.get_recent(limit)
    return jsonify(result), status

@dashboard_bp.route('/trends', methods=['GET'])
@role_required('analyst', 'viewer')
def trends():
    months = request.args.get('months', 12, type=int)
    result, status = DashboardController.get_trends(months)
    return jsonify(result), status