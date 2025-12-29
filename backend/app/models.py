from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

# ----------------- User Model -----------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    wishlist = relationship("Wishlist", back_populates="user", cascade="all, delete-orphan")
    borrow_records = relationship("BorrowRecord", back_populates="user", cascade="all, delete-orphan")

# ----------------- Book Model -----------------
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)
    category = Column(String, nullable=True)  # <-- New column

    # Borrow records for this book
    borrow_records = relationship("BorrowRecord", back_populates="book", cascade="all, delete-orphan")

# ----------------- Wishlist Model -----------------
class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    category = Column(String, nullable=True)  # <-- New column

    user = relationship("User", back_populates="wishlist")

# ----------------- BorrowRecord Model -----------------
class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)  # can be null if not returned yet

    status = Column(String, default="pending", nullable=False)  # <-- New column


    user = relationship("User", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")
