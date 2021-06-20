from flask import Blueprint, jsonify, request
from .. import cache


bp = Blueprint('metric', __name__)


@bp.route('/metric/<string:metric_key>', methods=('POST',))
def metric_post(metric_key):
    content = request.json
    if "value" not in content:
        return "Malformed POST data", 400

    cache.cache_item(metric_key, content["value"])
    return "OK", 200


@bp.route('/metric/<string:metric_key>/sum', methods=('GET',))
def metric_get(metric_key):
    key_data = cache.get_from_cache(metric_key)
    return jsonify(dict(value=sum_data(key_data)))


def sum_data(key_data: list[tuple]) -> int:
    return int(round(sum([x for (_, x) in key_data]), 0))
