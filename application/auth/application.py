from flask import Flask, request, jsonify
from configuration import Configuration
from models import database, User, Role, UserRole
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import and_
import re

application = Flask(__name__)
application.config.from_object(Configuration)

jwt = JWTManager(application)

def is_valid_email(email: str) -> bool:
    return re.fullmatch(r"[^@]+@[^@]+\.[^@]{2,}$", email or "") is not None

@application.route("/register_customer", methods=["POST"])
def register_customer():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")

    if forename is None or len(forename) == 0:
        return jsonify({"message": "Field forename is missing."}), 400
    if surname is None or len(surname) == 0:
        return jsonify({"message": "Field surname is missing."}), 400
    if email is None or len(email) == 0:
        return jsonify({"message": "Field email is missing."}), 400
    if password is None or len(password) == 0:
        return jsonify({"message": "Field password is missing."}), 400

    if not is_valid_email(email):
        return jsonify({"message": "Invalid email."}), 400

    if len(password) < 8:
        return jsonify({"message": "Invalid password."}), 400

    customerRole = Role.query.filter_by(name="customer").first()
    if customerRole is None:
        return jsonify({"message": "Role not configured."}), 400

    existing = User.query.filter_by(email=email).first()
    if existing is not None:
        return jsonify({"message": "Email already exists."}), 400

    user = User(email=email, password=password, firstname=forename, lastname=surname)
    database.session.add(user)
    database.session.commit()

    user_role = UserRole(id_role=customerRole.id, id_user=user.id)
    database.session.add(user_role)
    database.session.commit()

    return "", 200

@application.route("/register_courier", methods=["POST"])
def register_courier():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")

    if forename is None or len(forename) == 0:
        return jsonify({"message": "Field forename is missing."}), 400
    if surname is None or len(surname) == 0:
        return jsonify({"message": "Field surname is missing."}), 400
    if email is None or len(email) == 0:
        return jsonify({"message": "Field email is missing."}), 400
    if password is None or len(password) == 0:
        return jsonify({"message": "Field password is missing."}), 400

    if not is_valid_email(email):
        return jsonify({"message": "Invalid email."}), 400

    if len(password) < 8:
        return jsonify({"message": "Invalid password."}), 400

    courierRole = Role.query.filter_by(name="courier").first()
    if courierRole is None:
        return jsonify({"message": "Role not configured."}), 400

    existing = User.query.filter_by(email=email).first()
    if existing is not None:
        return jsonify({"message": "Email already exists."}), 400

    user = User(email=email, password=password, firstname=forename, lastname=surname)
    database.session.add(user)
    database.session.commit()

    user_role = UserRole(id_role=courierRole.id, id_user=user.id)
    database.session.add(user_role)
    database.session.commit()

    return "", 200

@application.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    if email is None or len(email) == 0:
        return jsonify({"message": "Field email is missing."}), 400
    if password is None or len(password) == 0:
        return jsonify({"message": "Field password is missing."}), 400

    if not is_valid_email(email):
        return jsonify({"message": "Invalid email."}), 400

    user = User.query.filter(and_(User.email == email, User.password == password)).first()
    if not user:
        return jsonify({"message": "Invalid credentials."}), 400

    additionalClaims = {
        "forename": user.firstname,
        "surname": user.lastname,
        "roles": [role.name for role in user.roles]
    }

    accessToken = create_access_token(identity=user.email, additional_claims=additionalClaims)
    return jsonify({"accessToken": accessToken}), 200

@application.route("/delete", methods=["POST"])
@jwt_required()
def delete():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Unknown user."}), 400

    try:
        database.session.delete(user)
        database.session.commit()
    except Exception:
        database.session.rollback()
        return jsonify({"message": "Database error."}), 400

    return "", 200

if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5002)