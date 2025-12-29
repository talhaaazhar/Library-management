from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import require_admin
from app.models import Book
from app.core.database import get_db
from app.schemas import BookCreate, BookRead, BookUpdate
from app.services.book_service import create_book , list_books, get_book, search_books, update_book,delete_book

Admin_books_router =APIRouter(
    prefix="/admin",
    tags=["admin-books"],
    dependencies= [Depends(require_admin)]
)

# ----------------- POST ROUTES -----------------
# add a book
@Admin_books_router.post('/books', response_model=BookRead)
async def admin_create_book(book: BookCreate, db: Session= Depends(get_db)):
    existing_book = db.query(Book).filter(
        Book.title == book.title,
        Book.author == book.author
    ).first()

    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Book with this title and author already exists."
        )
    
    return create_book(db, book)



# ----------------- GET ROUTES -----------------
# read all books
@Admin_books_router.get('/books', response_model=list[BookRead])
async def admin_read_all_books(db :Session= Depends(get_db)):
    return list_books(db)



#search book via title or author
@Admin_books_router.get('/books/search', response_model=list[BookRead])
async def admin_search_book(

    title: str= None,
    author: str= None, 
    db : Session= Depends(get_db)
):
    if not title and not author:
        raise HTTPException(
            status_code=400,
            detail="Provide at least title or author"
        )

    books = search_books(db, title, author)
    if not books:
        raise HTTPException(status_code=404, detail="No books found")

    return books



# read book by id 
@Admin_books_router.get('/books/{book_id}', response_model=BookRead, status_code=status.HTTP_200_OK)
async def admin_search_book(book_id: int , db:Session=Depends(get_db)):
    book=get_book(db , book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f'book with {book_id} not found ')
    return book



# ----------------- PUT ROUTES -----------------
@Admin_books_router.put('/book/{book_id}', response_model=BookRead)
async def admin_update_book(book_id: int, book : BookUpdate, db: Session=Depends(get_db)):
    updated_book= update_book(db , book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


# ----------------- DELETE ROUTES -----------------

@Admin_books_router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_book(book_id: int, db: Session = Depends(get_db)):
    if not delete_book(db, book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return