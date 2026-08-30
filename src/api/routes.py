from flask import jsonify

from src.api import bp

@bp.route("/test", methods=["GET"])
def test_api():
    return jsonify({
        "mensaje": "API funcionando satisfactoriamente"
    }), 200

