from db.database import SessionLocal


def get_db():
    """
    Create and provide a database session.

    Yields:
        Session: An SQLAlchemy database session.

    The session is closed automatically after
    the request is completed.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
