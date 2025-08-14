import sys
import os
import argparse

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from backend import config

print("Initializing database connection...")
print(f"Using DATABASE_URL: {config.DATABASE_URL}")


# --- 1) Normalize DATABASE_URL so SQLAlchemy loads the right dialect/driver ---
def normalize_db_url(url: str) -> str:
    """
    Ensure the URL uses a valid SQLAlchemy dialect.
    - Converts 'postgres://' -> 'postgresql+psycopg2://'
    - Optionally upgrades 'postgresql://' -> 'postgresql+psycopg2://'
      if you want to pin to psycopg2 (matches your earlier config).
    """
    if url.startswith("postgres://"):
        return "postgresql+psycopg2://" + url[len("postgres://"):]
    # If your env might be plain 'postgresql://', uncomment the next line to force psycopg2:
    # if url.startswith("postgresql://"):
    #     return "postgresql+psycopg2://" + url[len("postgresql://"):]
    return url

DATABASE_URL = normalize_db_url(config.DATABASE_URL)

# --- 2) Define Base BEFORE importing models to avoid circular import issues ---
class Base(DeclarativeBase):
    pass

# Now that Base exists, it's safe for models to import it from backend.db
# and safe for us to import models so metadata is populated.
from backend.models import entities  # noqa: E402,F401  (imports your model classes)

# --- 3) Create engine/session AFTER URL is normalized and models are imported ---
engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true")
    args = parser.parse_args()
    if args.init:
        init_db()
        print("✅ Database tables created.")
