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

@application.route("/search", methods=["GET"])
@jwt_required()
@roleCheck("customer")
def search():
    name_param = request.args.get("name", "") or ""
    category_param = request.args.get("category", "") or ""

    categories_q = (
        Category.query
        .outerjoin(ProductCategory, ProductCategory.id_category == Category.id)
        .outerjoin(Product,         Product.id == ProductCategory.id_product)
    )
    if name_param:
        categories_q = categories_q.filter(Product.name.like(f"%{name_param}%"))
    if category_param:
        categories_q = categories_q.filter(Category.name.like(f"%{category_param}%"))

    categories_raw = (
        categories_q
        .with_entities(Category.name)
        .distinct()
        .all()
    )
    categories = [name for (name,) in categories_raw]

    # products
    products_q = (
        database.session.query(
            Product.id.label("id"),
            Product.name.label("name"),
            Product.price.label("price"),
            func.group_concat(Category.name).label("cats_csv")
        )
        .select_from(Product)
        .outerjoin(ProductCategory, ProductCategory.id_product == Product.id)
        .outerjoin(Category,        Category.id == ProductCategory.id_category)
    )
    if name_param:
        products_q = products_q.filter(Product.name.like(f"%{name_param}%"))
    if category_param:
        products_q = products_q.filter(Category.name.like(f"%{category_param}%"))

    products_raw = (
        products_q
        .group_by(Product.id, Product.name, Product.price)
        .all()
    )

    products = []
    for id, name, price, cats_csv in products_raw:
        product_categories = cats_csv.split(",") if cats_csv else []
        products.append({
            "id": id,
            "name": name,
            "price": float(price),
            "categories": product_categories
        })

    return jsonify({"categories": categories, "products": products}), 200

@application.route("/order", methods=["POST"])
@jwt_required()
@roleCheck("customer")
def order():
    requests = request.json.get("requests", None)

    identity = get_jwt_identity()

    #provera uslova iz zadatka
    if requests is None:
        return jsonify({"message": "Field requests is missing."}), 400

    for request_id, single_request in enumerate(requests):
        if "id" not in single_request:
            return jsonify({"message": f"Product id is missing for request number {request_id}."}), 400
        elif "quantity" not in single_request:
            return jsonify({"message": f"Product quantity is missing for request number {request_id}."}), 400
        elif not isinstance(single_request["id"], int) or single_request["id"] <= 0:
            return jsonify({"message": f"Invalid product id for request number {request_id}."}), 400
        elif not isinstance(single_request["quantity"], int) or single_request["quantity"] <= 0:
            return jsonify({"message": f"Invalid product quantity for request number {request_id}."}), 400
        elif Product.query.filter_by(id=single_request["id"]).first() is None:
            return jsonify({"message": f"Invalid product for request number {request_id}."}), 400

    #dodavanje proizvoda
    new_order = Order(status="CREATED", ordered_by=identity)
    database.session.add(new_order)
    database.session.commit()

    for single_request in requests:
        existing_order_product = OrderProduct.query.filter_by(id_product=single_request["id"], id_order=new_order.id).first()
        if existing_order_product is None:
            new_order_product = OrderProduct(id_order=new_order.id, id_product=single_request["id"], amount=single_request["quantity"])
            database.session.add(new_order_product)
            database.session.commit()
        else:
            existing_order_product.amount += single_request["quantity"]

    database.session.commit()
    return jsonify({"id": new_order.id}), 200

@application.route("/status", methods=["GET"])
@jwt_required()
@roleCheck("customer")
def status():
    identity = get_jwt_identity()

    orders_raw = (
        database.session.query(
            Order.id,
            func.coalesce(func.sum(OrderProduct.amount * Product.price), 0).label("price"),
            Order.status,
            Order.creation_timestamp,
        )
        .select_from(Order)
        .filter(Order.ordered_by == identity)
        .outerjoin(OrderProduct, OrderProduct.id_order == Order.id)
        .outerjoin(Product, Product.id == OrderProduct.id_product)
        .group_by(Order.id, Order.status, Order.creation_timestamp)
        .all()
    )

    orders = []
    for id_order, price, status, creation_timestamp in orders_raw:
        products_raw = Order.query.get(id_order).products

        products = []
        for product in products_raw:
            order_product = OrderProduct.query.filter_by(id_product=product.id, id_order=id_order).first()
            products.append({
                "categories": [category.name for category in product.categories],
                "name": product.name,
                "price": float(product.price),
                "quantity": int(order_product.amount)
            })

        orders.append({
            "products": products,
            "price": float(price),
            "status": status,
            "timestamp": creation_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        })

    return jsonify({"orders": orders}), 200

@application.route("/delivered", methods=["POST"])
@jwt_required()
@roleCheck("customer")
def delivered():
    id = request.json.get("id", None)

    if id is None:
        return jsonify({"message": "Missing order id."}), 400
    if not isinstance(id, int) or id <= 0:
        return jsonify({"message": "Invalid order id."}), 400

    order = Order.query.filter_by(id=id).first()

    if (order is None):
        return jsonify({"message": "Invalid order id."}), 400
    if order.status == "CREATED":
        return jsonify({"message": "Delivery not complete."}), 400

    order.status = "COMPLETE"
    database.session.commit()

    return Response(status=200)

if (__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5004)