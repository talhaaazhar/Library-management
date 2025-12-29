from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import require_admin
from app.services.wishlist_service import (
    list_all_wishlists,
    delete_wishlist_item,
    update_wishlist_item
)
from app.schemas import WishlistRead, WishlistUpdate
from app.models import User


router = APIRouter(
    prefix="/admin/wishlist",
    tags=["admin-wishlist"],
    dependencies=[Depends(require_admin)]
)


# List all wishlists
@router.get("/", response_model=list[WishlistRead])
def admin_list_all_wishlists(db: Session = Depends(get_db)):
    return list_all_wishlists(db)

# Delete any wishlist item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_wishlist(item_id: int, db: Session = Depends(get_db)):
    if not delete_wishlist_item(db, item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return


# ------------------- EDIT ANY WISHLIST ITEM (ADMIN) -------------------
@router.patch("/{item_id}", response_model=WishlistRead)
def admin_update_wishlist(item_id: int, data: WishlistUpdate, db: Session = Depends(get_db)):
    updated_item = update_wishlist_item(db, item_id, data)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item