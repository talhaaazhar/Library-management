from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import require_admin
from app.services.borrow_service import list_all_borrows, admin_return_book
from app.schemas import BorrowRead
router = APIRouter(
    prefix="/admin/borrow",
    tags=["admin-borrow"],
    dependencies=[Depends(require_admin)]
)


# List all borrow records
@router.get('/')
async def admin_list_borrows(db: Session = Depends(get_db)):
    return list_all_borrows(db)


# Force too return a book
@router.put("/return/{borrow_id}")
def admin_return_borrow(borrow_id: int, db: Session = Depends(get_db)):
    try:
        borrow = admin_return_book(db, borrow_id)
        return borrow
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))