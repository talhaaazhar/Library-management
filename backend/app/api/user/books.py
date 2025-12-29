from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.database import get_db
from app.schemas import BookRead
from app.services.book_service import list_books, search_books, get_book
from app.dependencies import require_user

user_books_router = APIRouter(
    prefix="/books",
    tags=["user-books"],
    dependencies=[Depends(require_user)]  # ensures only logged-in users
)


# Get all books
@user_books_router.get("/", response_model=List[BookRead])
async def get_all_books(db: Session = Depends(get_db)):
    return list_books(db)


# Search books by title or author
@user_books_router.get("/search", response_model=List[BookRead])
async def search_books_endpoint(
    title: Optional[str] = None,
    author: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if not title and not author:
        raise HTTPException(status_code=400, detail="Provide at least title or author")
    
    results = search_books(db, title, author)
    if not results:
        raise HTTPException(status_code=404, detail="No books found")
    
    return results


# Get book by ID
@user_books_router.get("/{book_id}", response_model=BookRead)
async def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return book
