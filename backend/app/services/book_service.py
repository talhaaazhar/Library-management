from sqlalchemy.orm import Session
from app.models import Book
from app.schemas import BookCreate, BookRead, BookUpdate

# admin CRUD operations for books

def create_book(db: Session, book_data: BookCreate) -> Book:
    new_book=Book(
        title=book_data.title,
        author=book_data.author,
        year=book_data.year,
        total_copies=book_data.total_copies,
        available_copies=book_data.total_copies
       )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def list_books(db: Session):
    books = db.query(Book).all()
    return books


def get_book(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


def search_books(db: Session, title : str= None, author : str= None )-> list[Book]:
    query=db.query(Book)
    if title:
        query= query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query=query.filter(Book.author.ilike(f"%{author}%"))

    return query.all()


def update_book(db: Session, book_id: int, book_data: BookUpdate)-> Book| None:
    existing_book=get_book(db, book_id)

    if not existing_book:
        return None
    

    # existing_book.title=book.title
    # existing_book.author=book.author
    # existing_book.year=book.year
    # existing_book.available_copies=book.available_copies
    # existing_book.total_copies=book.total_copies

        # Update only fields provided
    for field, value in book_data.dict(exclude_unset=True).items():
        setattr(existing_book, field, value)


    # Ensure available_copies never exceeds total_copies
    if existing_book.available_copies > existing_book.total_copies:
        existing_book.available_copies = existing_book.total_copies

    db.commit()
    db.refresh(existing_book)
    return existing_book




def delete_book(db: Session, book_id)->bool:
    book= db.query(Book).filter(Book.id==book_id).first()
    if not book:
        return False
    db.delete(book)
    db.commit()
    return True

