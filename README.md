# Store Management System (Flask + SQLAlchemy + Docker)

## 📌 Overview
This project is a **multi-user store management system** implemented as part of the **Electronic Business Infrastructure** course.  
It allows **customers, couriers, and store owners** to interact with the store through REST APIs, with secure authentication and authorization using **JWT tokens**.  
The system is containerized with **Docker** and orchestrated via **Docker Compose** for modular deployment.

## 🚀 Features

### User Management
- Register as customer or courier  
- Login and obtain JWT access tokens  
- Delete user accounts  

### Customer Functionality
- Search products by name or category  
- Place orders  
- View order status (Created, Pending, Completed)  

### Courier Functionality
- View available orders for delivery  
- Pick up orders and mark them as delivered  

### Owner Functionality
- Add new products via CSV upload  
- View product sales statistics  
- View category statistics  

## 🛠️ Technologies Used
- Python 3  
- Flask (web framework)  
- SQLAlchemy (ORM)  
- JWT (Flask-JWT-Extended) for authentication & authorization  
- Docker & Docker Compose (service orchestration)  
- MySQL (database)  

## 🖥️ Services
The system consists of the following services:
- **Auth service** – user registration, login, account deletion  
- **Owner service** – product management and sales/category statistics  
- **Customer service** – product search, orders, and status  
- **Courier service** – delivery management  

**Notes:**
- Databases are initialized automatically when containers are started.  
- External database access is disabled for security reasons.  
- Each microservice is isolated and communicates only via its defined API.
