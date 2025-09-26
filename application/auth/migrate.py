from flask import Flask
from configuration import Configuration
from flask_migrate import Migrate, init, migrate, upgrade
from models import database, User, Role
from sqlalchemy_utils import database_exists, create_database

application = Flask(__name__)
application.config.from_object(Configuration)

migrateObject = Migrate(application, database)

if (not database_exists(application.config["SQLALCHEMY_DATABASE_URI"])):
    create_database(application.config["SQLALCHEMY_DATABASE_URI"])

database.init_app(application)

with application.app_context() as context:
    init()
    migrate(message="Production migration")
    upgrade()

    ownerRole = Role(name="owner")
    customerRole = Role(name="customer")
    courierRole = Role(name="courier")

    database.session.add(ownerRole)
    database.session.add(customerRole)
    database.session.add(courierRole)
    database.session.commit()

    dbOwnerRole = Role.query.filter_by(name="owner").first()
    owner = User(
        email="onlymoney@gmail.com",
        password="evenmoremoney",
        firstname="Scrooge",
        lastname="McDuck"
    )

    owner.roles.append(dbOwnerRole)

    database.session.add(owner)
    database.session.commit()