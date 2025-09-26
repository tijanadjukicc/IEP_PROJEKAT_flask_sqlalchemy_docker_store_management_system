from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, ForeignKey, UniqueConstraint

database = SQLAlchemy()

class UserRole(database.Model):
    __tablename__ = "user_role"

    id = database.Column(database.Integer, primary_key=True)
    id_role = database.Column(database.Integer, ForeignKey("role.id", ondelete="CASCADE"), nullable=False)
    id_user = database.Column(database.Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("id_user", "id_role", name="uq_user_role_pair"),
    )

class Role(database.Model):
    __tablename__ = "role"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(
        Enum("customer", "courier", "owner", name="role_name"),
        unique=True,
        nullable=False
    )

    users = database.relationship(
        "User",
        secondary=UserRole.__table__,
        back_populates="roles",
        lazy="selectin"
    )

class User(database.Model):
    __tablename__ = "user"

    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(256), nullable=False, unique=True)
    password = database.Column(database.String(256), nullable=False)
    firstname = database.Column(database.String(256), nullable=False)
    lastname = database.Column(database.String(256), nullable=False)

    roles = database.relationship(
        "Role",
        secondary=UserRole.__table__,
        back_populates="users",
        lazy="selectin"
    )