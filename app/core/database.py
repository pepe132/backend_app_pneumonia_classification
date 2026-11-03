from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import DB_NAME, DB_PASSWORD, DB_PORT, DB_SERVER, DB_USER


def build_database_url() -> str:
    required_values = {
        "DB_SERVER": DB_SERVER,
        "DB_NAME": DB_NAME,
        "DB_USER": DB_USER,
        "DB_PASSWORD": DB_PASSWORD,
    }
    missing_values = [name for name, value in required_values.items() if not value]
    if missing_values:
        raise ValueError(
            "Faltan variables de entorno para la base de datos: "
            + ", ".join(missing_values)
        )

    user = quote_plus(DB_USER)
    password = quote_plus(DB_PASSWORD)
    server = DB_SERVER
    port = DB_PORT or "1433"
    database = quote_plus(DB_NAME)

    return f"mssql+pymssql://{user}:{password}@{server}:{port}/{database}"


DATABASE_URL = build_database_url()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
