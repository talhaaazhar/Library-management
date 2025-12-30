from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.borrow_service import borrow_book, return_book, list_user_borrows

router = APIRouter(
    prefix="/borrow",
    tags=["user-borrow"]
)

# Borrow a book
@router.post("/{book_id}")
def user_borrow_book(book_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        borrow = borrow_book(db, current_user.id, book_id)
        return borrow
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Return a book
@router.put("/return/{borrow_id}")
def user_return_book(borrow_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        borrow = return_book(db, borrow_id, current_user.id)
        return borrow
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# List my borrows
@router.get("/")
def user_list_borrows(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return list_user_borrows(db, current_user.id)
