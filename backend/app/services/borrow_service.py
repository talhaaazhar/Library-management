from sqlalchemy.orm import Session
from datetime import datetime
from app.models import BorrowRecord, Book

# ------------------- BORROW A BOOK -------------------
def borrow_book(db: Session, user_id: int, book_id: int) -> BorrowRecord:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise ValueError("Book not found")
    if book.available_copies < 1:
        raise ValueError("No available copies to borrow")

    # Reduce available copies
    book.available_copies -= 1

    borrow = BorrowRecord(
        user_id=user_id,
        book_id=book_id,
        status="borrowed",
        borrow_date=datetime.utcnow()
    )
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow


# ------------------- RETURN A BOOK -------------------
def return_book(db: Session, borrow_id: int) -> BorrowRecord:
    borrow = db.query(BorrowRecord).filter(BorrowRecord.id == borrow_id).first()
    if not borrow:
        raise ValueError("Borrow record not found")
    if borrow.status != "borrowed":
        raise ValueError("Book already returned")

    borrow.return_date = datetime.utcnow()
    borrow.status = "returned"

    # Update book available copies
    book = borrow.book
    book.available_copies += 1

    db.commit()
    db.refresh(borrow)
    return borrow


# ------------------- LIST BORROW RECORDS FOR USER -------------------
def list_user_borrows(db: Session, user_id: int):
    return db.query(BorrowRecord).filter(BorrowRecord.user_id == user_id).all()


# ------------------- LIST ALL BORROW RECORDS (ADMIN) -------------------
def list_all_borrows(db: Session):
    return db.query(BorrowRecord).all()


# ------------------- ADMIN FORCE RETURN -------------------
def admin_return_book(db: Session, borrow_id: int):
    borrow = db.query(BorrowRecord).filter(BorrowRecord.id == borrow_id).first()
    if not borrow:
        raise ValueError("Borrow record not found")
    if borrow.status != "borrowed":
        raise ValueError("Book already returned")

    borrow.return_date = datetime.utcnow()
    borrow.status = "returned"

    borrow.book.available_copies += 1

    db.commit()
    db.refresh(borrow)
    return borrow
