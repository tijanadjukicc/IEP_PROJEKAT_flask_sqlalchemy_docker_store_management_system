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

@application.route("/update", methods=["POST"])
@jwt_required()
@roleCheck("owner")
def update_products():
    if "file" not in request.files:
        return jsonify({"message": "Field file is missing."}), 400

    file_content = request.files["file"].stream.read().decode("utf-8")
    stream = io.StringIO(file_content)
    reader = csv.reader(stream)

    rows = []
    for line_number, row in enumerate(reader):
        if (len(row) != 3):
            return jsonify({"message": f"Incorrect number of values on line {line_number}."}), 400

        #row content
        categories = row[0].split("|")
        name = row[1]

        try:
            price = float(row[2])
        except Exception:
            return jsonify({"message": f"Incorrect price on line {line_number}."}), 400

        if (price <= 0):
            return jsonify({"message": f"Incorrect price on line {line_number}."}), 400

        product = Product.query.filter_by(name=name).first()

        if (product is not None):
            return jsonify({"message": f"Product {name} already exists."}), 400

        rows.append((name, categories, price))

    for row in rows:
        #row content
        name = row[0]
        categories = row[1]
        price = row[2]

        product = Product(name=name, price=price)
        database.session.add(product)
        database.session.flush()

        for category in categories:
            category_object = Category.query.filter_by(name=category).first()

            if (category_object is None):
                category_object = Category(name=category)
                database.session.add(category_object)
                database.session.flush()

            product_category_object = ProductCategory.query.filter(and_(
                ProductCategory.id_product == product.id,
                ProductCategory.id_category == category_object.id
            )).first()

            if (product_category_object is None):
                product_category_object = ProductCategory(id_product=product.id, id_category=category_object.id)
                database.session.add(product_category_object)
                database.session.flush()

    database.session.commit()

    return Response(status=200)

@application.route("/product_statistics", methods=["GET"])
@jwt_required()
@roleCheck("owner")
def product_statistics():
    rows = Product.query.join(OrderProduct).join(Order).group_by(Product.id).with_entities(
        Product.name.label("name"),
        func.sum(func.if_(Order.status == "COMPLETE", OrderProduct.amount, 0)).label("sold"),
        func.sum(func.if_(Order.status == "CREATED", OrderProduct.amount, 0)).label("waiting")
    ).all()

    statistics = [
        {"name": name, "sold": int(sold or 0), "waiting": int(waiting or 0)}
        for name, sold, waiting in rows
    ]

    return jsonify({"statistics": statistics}), 200

@application.route("/category_statistics", methods=["GET"])
@jwt_required()
@roleCheck("owner")
def category_statistics():
    delivered = func.coalesce(
        func.sum(func.if_(Order.status == "COMPLETE", OrderProduct.amount, 0)),
        0
    ).label("delivered")

    rows = (
        database.session.query(Category.name.label("name"), delivered)
        .select_from(Category)
        .outerjoin(ProductCategory, ProductCategory.id_category == Category.id)
        .outerjoin(Product,         Product.id == ProductCategory.id_product)
        .outerjoin(OrderProduct,    OrderProduct.id_product == Product.id)
        .outerjoin(Order,           Order.id == OrderProduct.id_order)
        .group_by(Category.id, Category.name)
        .order_by(delivered.desc(), Category.name.asc())
        .all()
    )

    statistics = [name for name, _ in rows]
    return jsonify({"statistics": statistics}), 200

if (__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5003)