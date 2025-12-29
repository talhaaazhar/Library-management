from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.core.database import get_db
from app.dependencies import require_admin
from app.schemas import (
    UserRead,
    UserStatusUpdate,
    UserRoleUpdate,
    PasswordChangeRequest
)
from app.services.user_service import (
    list_users,
    get_user_by_id,
    update_user_status,
    update_user_role,
    delete_user,
    change_user_password
)
from app.models import User

router = APIRouter(
    prefix="/admin/users",
    tags=["admin-users"],
    dependencies=[Depends(require_admin)]
)

# ------------------- LIST USERS -------------------
@router.get("/", response_model=list[UserRead])
def admin_list_users(db: Session = Depends(get_db)):
    return list_users(db)


# ------------------- GET USER -------------------
@router.get("/{user_id}", response_model=UserRead)
def admin_get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ------------------- ACTIVATE / SUSPEND -------------------
@router.patch("/{user_id}/status", response_model=UserRead)
def admin_update_user_status(
    user_id: int,
    data: UserStatusUpdate,
    db: Session = Depends(get_db)
):
    user = update_user_status(db, user_id, data.is_active)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ------------------- CHANGE ROLE -------------------
@router.patch("/{user_id}/role", response_model=UserRead)
def admin_update_user_role(
    user_id: int,
    data: UserRoleUpdate,
    db: Session = Depends(get_db)
):
    user = update_user_role(db, user_id, data.role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ------------------- DELETE USER -------------------
# @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def admin_delete_user(user_id: int, db: Session = Depends(get_db)):
#     if not delete_user(db, user_id):
#         raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Admin cannot delete themselves"
        )

    if not delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    


    #change password 
@router.put("/me/password", status_code=status.HTTP_200_OK)
def admin_change_own_password(
    data: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user, error = change_user_password(db, current_user.id, data.old_password, data.new_password)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"detail": "Password updated successfully"}