from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from ..config import DATABASE_URL


class Base(DeclarativeBase):
	pass


# For SQLite, need check_same_thread=False; SQLAlchemy parses it from URL params; keep simple.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

