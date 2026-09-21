from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.config import Settings, get_settings


settings = get_settings()
SQLALCHEMY_DATABASE_URL = '{0}://{1}:{2}@{3}:{4}/{5}?sslmode=disable'.format(
    settings.DB_CONNECTION,
    settings.DB_USERNAME,
    settings.DB_PASSWORD,
    settings.DB_HOST,
    settings.DB_PORT,
    settings.DB_DATABASE
)

# , connect_args={"check_same_thread": False}
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_database() -> None:
    """
    Create all database tables defined in the SQLAlchemy models.

    This function creates the database tables that do not
    already exist based on the metadata registered in Base.
    """
    Base.metadata.create_all(bind=engine)
