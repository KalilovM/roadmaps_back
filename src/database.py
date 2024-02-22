from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from src.config import SQL_ALCHEMY_DB_URL

engine = create_engine(
    SQL_ALCHEMY_DB_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

