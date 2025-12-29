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



@router.get('/', response_model=BorrowRead)
async def admin_list_borrows(db: Session = Depends(get_db)):
    return list_all_borrows(db)


