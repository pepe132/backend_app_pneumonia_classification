import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Neumonia Platform")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")

SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

if not SECRET_KEY:
    raise ValueError("SECRET_KEY no está configurada en el archivo .env")