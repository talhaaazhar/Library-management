from sqlalchemy.orm import Session
from app.models import User
from app.core.security import verify_password, hash_password

def list_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user_status(db: Session, user_id: int, is_active: bool):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user


def update_user_role(db: Session, user_id: int, role: str):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.role = role
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False

    db.delete(user)
    db.commit()
    return True



def change_user_password(db: Session, user_id: int, old_password: str, new_password: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None, "User not found"

    # verify old password
    if not verify_password(old_password, user.password):
        return None, "Old password is incorrect"

    user.password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user, None
