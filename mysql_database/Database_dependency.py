# =========================================================
# DATABASE DEPENDENCY
# =========================================================
# Provides DB session to API routes
# Automatically closes session after request
from database import SessionLocal

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()