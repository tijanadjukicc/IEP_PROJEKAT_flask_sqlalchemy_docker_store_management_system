from flask import Flask, request, jsonify, Response
from sqlalchemy       import desc
from sqlalchemy       import and_
from sqlalchemy       import or_
from sqlalchemy       import between
from sqlalchemy       import distinct
from sqlalchemy       import func
from sqlalchemy       import not_
from sqlalchemy.orm   import aliased
from configuration import Configuration
from models import *
import io
import csv
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity
from decorator import roleCheck

application = Flask(__name__)
application.config.from_object(Configuration)

jwt = JWTManager(application)

@application.route("/orders_to_deliver", methods=["GET"])
@jwt_required()
@roleCheck("courier")
def orders_to_deliver():

    raw_orders = (
        Order.query
        .with_entities(Order.id, Order.ordered_by)
        .filter(Order.status == "CREATED")
        .all()
    )

    orders = []
    for id, email in raw_orders:
        orders.append({
            "id": id,
            "email": email
        })

    return jsonify({"orders": orders}), 200

@application.route("/pick_up_order", methods=["POST"])
@jwt_required()
@roleCheck("courier")
def pick_up_order():
    id = request.json.get("id", None)

    if id is None:
        return jsonify({"message": "Missing order id."}), 400
    elif not isinstance(id, int) or id <=0:
        return jsonify({"message": "Invalid order id."}), 400

    order = Order.query.filter_by(id=id).first()

    if order is None or order.status != "CREATED":
        return jsonify({"message": "Invalid order id."}), 400

    order.status = "PENDING"
    database.session.commit()

    return Response(status=200)

if (__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5005)