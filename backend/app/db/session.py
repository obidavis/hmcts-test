from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# TODO: Replace with actual database URL
DATABASE_URL = "sqlite:///temp.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()