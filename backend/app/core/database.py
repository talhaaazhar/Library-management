# app/core/database.py
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings  # <-- load from .env
from app.core.logger import logger

# Do not echo SQL by default (avoids noisy logs on every server start).
engine = create_engine(settings.DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_tables(verbose: bool = False):
    """Create DB tables.

    If the `users` table does not exist this is assumed to be a fresh DB; in
    that case, if `verbose` is True SQL statements will be echoed so you can
    see the CREATE statements. On subsequent runs tables are created quietly
    and only a simple message is logged.
    """
    from app.models import User, Book, BorrowRecord, Wishlist

    insp = inspect(engine)
    users_exists = insp.has_table("users")

    if not users_exists and verbose:
        # show SQL when we actually create the schema for the first time
        tmp_engine = create_engine(settings.DATABASE_URL, echo=True)
        Base.metadata.create_all(bind=tmp_engine)
        logger.info("Database schema created (verbose SQL output shown).")
        print("All tables created successfully!")
    else:
        # quiet creation or ensuring schema exists
        Base.metadata.create_all(bind=engine)
        if not users_exists:
            logger.info("Database schema created.")
        else:
            logger.info("Database already initialized; tables present.")
        print("All tables created successfully!")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Auto-create tables on import but remain quiet; pass verbose=True if you
# want to see SQL the first time you initialize the DB.
create_tables()
