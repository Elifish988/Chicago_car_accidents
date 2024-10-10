from datetime import datetime

from flask import Blueprint, jsonify, request

from repository.querys_repository import count_accidents_by_region, count_accidents_by_region_and_period

bp_query = Blueprint('bp_query', __name__)


@bp_query.route('/accidents/<region>', methods=['GET'])
def get_accidents_by_region(region):
    total = count_accidents_by_region(region)
    return jsonify({"region": region, "total_accidents": total})


@bp_query.route('/accidents_by_period/<region>', methods=['GET'])
def get_accidents_by_region_and_period(region):
    period = request.args.get('period')
    start_date = request.args.get('start_date')

    if not region or not period or not start_date:
        return jsonify({"error": "Region, period, and start_date are required"}), 400


    total = count_accidents_by_region_and_period(region, period, start_date)

    if isinstance(total, dict) and 'error' in total:
        return jsonify(total), 400

    return jsonify({"region": region, "period": period, "start_date": start_date, "total_accidents": total})