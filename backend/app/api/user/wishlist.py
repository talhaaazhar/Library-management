from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import require_user
from app.services.wishlist_service import (
    add_to_wishlist, 
    list_wishlist,
      delete_wishlist_item,
      update_wishlist_item
)
from app.schemas import WishlistCreate, WishlistRead, WishlistUpdate
from app.models import User
from app.core.security import get_current_user


router = APIRouter(
    prefix="/wishlist",
    tags=["user-wishlist"],
    dependencies=[Depends(require_user)]
)

# Add item
@router.post("/", response_model=WishlistRead)
def user_add_to_wishlist(data: WishlistCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return add_to_wishlist(db, current_user.id, data)

# List items
@router.get("/", response_model=list[WishlistRead])
def user_list_wishlist(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_wishlist(db, current_user.id)

# Delete item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def user_delete_wishlist(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not delete_wishlist_item(db, item_id, current_user.id):
        raise HTTPException(status_code=404, detail="Item not found")
    return


# ------------------- EDIT OWN WISHLIST ITEM -------------------
@router.patch("/{item_id}", response_model=WishlistRead)
def user_update_wishlist(item_id: int, data: WishlistUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_item = update_wishlist_item(db, item_id, data, user_id=current_user.id)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


