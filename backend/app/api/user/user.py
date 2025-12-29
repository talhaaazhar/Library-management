from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import PasswordChangeRequest
from app.models import User
from app.services.user_service import change_user_password
from app.dependencies import require_user
from app.core.security import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["user-account"],
    dependencies=[Depends(require_user)]

)

@router.put("/password", status_code=status.HTTP_200_OK)
def update_password(
    data: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user :User = Depends(get_current_user)
):
    user, error = change_user_password(db, current_user.id, data.old_password, data.new_password)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"detail": f"Password of {user.name} updated successfully"}