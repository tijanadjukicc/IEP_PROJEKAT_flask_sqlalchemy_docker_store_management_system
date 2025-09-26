from datetime import timedelta
import os

databaseUrl = os.environ["DATABASE_URL"]

class Configuration:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/store_db"
    JWT_SECRET_KEY = "8f9a7c2e4d1b6a5f3c9d8e7f0a2b4c6d1e3f5a7b9c0d2e4f6a8b0c2d4e6f8a0"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)