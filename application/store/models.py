from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, Numeric, UniqueConstraint, ForeignKey
from datetime import datetime

database = SQLAlchemy()

class ProductCategory(database.Model):
    __tablename__ = "product_categories"
    id = database.Column(database.Integer, primary_key=True)
    id_category = database.Column(database.Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    id_product  = database.Column(database.Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

class Category(database.Model):
    __tablename__ = "categories"
    id   = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False, unique=True)

    products = database.relationship(
        "Product",
        secondary=ProductCategory.__table__,
        back_populates="categories",
        lazy="selectin"
    )

class OrderProduct(database.Model):
    __tablename__ = "order_products"
    id         = database.Column(database.Integer, primary_key=True)
    id_order   = database.Column(database.Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    id_product = database.Column(database.Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    amount     = database.Column(database.Integer, nullable=False)

    # veze ka parentima (asocijacioni objekat)
    order   = database.relationship("Order",   back_populates="items")
    product = database.relationship("Product", back_populates="order_items")

    __table_args__ = (
        UniqueConstraint("id_order", "id_product", name="uq_order_product_pair"),  # opciono, ali korisno
    )

class Product(database.Model):
    __tablename__ = "products"
    id    = database.Column(database.Integer, primary_key=True)
    name  = database.Column(database.String(256), nullable=False, unique=True)
    price = database.Column(Numeric(10, 2), nullable=False)

    categories  = database.relationship("Category", secondary=ProductCategory.__table__, back_populates="products", lazy="selectin")

    # 1:N ka stavkama narudžbina
    order_items = database.relationship("OrderProduct", back_populates="product", cascade="all, delete-orphan", lazy="selectin")

    # M2M ka narudžbinama preko order_products
    orders = database.relationship("Order", secondary="order_products", back_populates="products", lazy="selectin")

class Order(database.Model):
    __tablename__ = "orders"
    id                  = database.Column(database.Integer, primary_key=True)
    ordered_by          = database.Column(database.String(256), nullable=False)
    status              = database.Column(Enum("CREATED", "PENDING", "COMPLETE", name="order_status"), nullable=False, default="CREATED")
    creation_timestamp  = database.Column(database.DateTime, default=datetime.utcnow, nullable=False)

    # 1:N ka stavkama
    items   = database.relationship("OrderProduct", back_populates="order", cascade="all, delete-orphan", lazy="selectin")

    # M2M ka proizvodima
    products = database.relationship("Product", secondary="order_products", back_populates="orders", lazy="selectin")
