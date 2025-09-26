# Store Management System (Flask + SQLAlchemy + Docker)

<h1>📌 Overview</h1>

This project is a multi-user store management system implemented as part of the IEP course.
It allows customers, couriers, and store owners to interact with the store through REST APIs, with secure authentication and authorization using JWT tokens.
The system is containerized with Docker and orchestrated via Docker Compose for modular deployment.

<h1>🚀 Features<h1>

<h2>User Management</h2>

Register as customer or courier

Login and obtain JWT access tokens

Delete user accounts

<h2>Customer Functionality</h2>

Search products by name or category

Place orders

View order status (Created, Pending, Completed)

<h2>Courier Functionality</h2>

View available orders for delivery

Pick up orders and mark them as delivered

<h2>Owner Functionality</h2>

Add new products via CSV upload

View product sales statistics

View category statistics

<h1>🛠️ Technologies Used</h1>

Python 3

Flask (web framework)

SQLAlchemy (ORM)

JWT (Flask-JWT-Extended) for authentication & authorization

Docker & Docker Compose (service orchestration)

MySQL (database)
