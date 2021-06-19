from flask import Blueprint, jsonify, request
from .. import cache


bp = Blueprint('metric', __name__)


@bp.route('/metric/<string:metric_key>', methods=('GET', 'POST'))
def register(metric_key):
    if request.method == 'POST':
        content = request.json
        if "value" not in content:
            return "Malformed POST data", 400

        cache.cache_item(metric_key, content["value"])
        return "OK", 200
    else:  # GET
        key_data = cache.get_from_cache(metric_key)
        return jsonify(dict(value=sum_data(key_data)))


def sum_data(key_data: list[tuple]) -> int:
    return int(round(sum([x for (_, x) in key_data]), 0))
