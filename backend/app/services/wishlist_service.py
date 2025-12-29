from sqlalchemy.orm import Session
from app.models import Wishlist
from app.schemas import WishlistCreate, WishlistRead,WishlistUpdate

# ------------------- CREATE WISHLIST ITEM -------------------
def add_to_wishlist(db: Session, user_id: int, data: WishlistCreate) -> Wishlist:
    item = Wishlist(
        user_id=user_id,
        book_name=data.book_name,
        description=data.description
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# ------------------- LIST WISHLIST ITEMS FOR A USER -------------------
def list_wishlist(db: Session, user_id: int):
    return db.query(Wishlist).filter(Wishlist.user_id == user_id).all()


# ------------------- LIST ALL WISHLIST ITEMS (ADMIN) -------------------
def list_all_wishlists(db: Session):
    return db.query(Wishlist).all()

# ------------------- DELETE WISHLIST ITEM -------------------
# def delete_wishlist_item(db: Session, item_id: int) -> bool:
#     item = db.query(Wishlist).filter(Wishlist.id == item_id).first()
#     if not item:
#         return False
#     db.delete(item)
#     db.commit()
#     return True



# def delete_wishlist_user_item( db: Session, item_id: int, current_user_id: int )->bool:
#     item = db.query(Wishlist).filter(Wishlist.id == item_id, Wishlist.user_id == current_user_id).first()
#     return delete_wishlist_item(db, item.id)


def delete_wishlist_item(db: Session, item_id: int, user_id: int = None) -> bool:
    """
    Deletes a wishlist item.
    If user_id is provided, ensures the item belongs to that user.
    Returns True if deleted, False if not found.
    """
    query = db.query(Wishlist).filter(Wishlist.id == item_id)
    if user_id is not None:
        query = query.filter(Wishlist.user_id == user_id)
    
    item = query.first()
    if not item:
        return False

    db.delete(item)
    db.commit()
    
    return True



def update_wishlist_item(db: Session, item_id: int, data: WishlistUpdate, user_id: int = None) -> Wishlist | None:
    """
    Updates a wishlist item. 
    If user_id is provided, ensures the item belongs to that user.
    """
    query = db.query(Wishlist).filter(Wishlist.id == item_id)
    if user_id is not None:
        query = query.filter(Wishlist.user_id == user_id)
    
    item = query.first()
    if not item:
        return None

    # Update only provided fields
    for field, value in data.dict(exclude_unset=True).items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    return item