from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# ------------------- USER -------------------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str =Field(min_length=6)

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        orm_mode = True



class UserStatusUpdate(BaseModel):
    is_active: bool


class UserRoleUpdate(BaseModel):
    role: str = Field(pattern="^(user|admin)$")



class PasswordChangeRequest(BaseModel):
    old_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)


    
# ------------------- BOOK -------------------
class BookCreate(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    total_copies: int = 1
    category: Optional[str] = None  # <-- New

class BookRead(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int] = None
    total_copies: int
    available_copies: int
    category: Optional[str] = None  # <-- New

    class Config:
        orm_mode = True

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    total_copies: Optional[int] = None
    available_copies: Optional[int] = None
    category: Optional[str] = None  # <-- New

# ------------------- BORROW -------------------
class BorrowRequest(BaseModel):
    book_id: int

class BorrowRead(BaseModel):
    id: int
    user_id: int
    book_id: int
    status: str  # pending | approved | returned
    request_date: datetime
    approve_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    

    class Config:
        orm_mode = True

# ------------------- WISHLIST -------------------
class WishlistCreate(BaseModel):
    book_name: str
    description: Optional[str] = None
    category: Optional[str] = None  # <-- New

class WishlistRead(BaseModel):
    id: int
    user_id: int
    book_name: str
    description: Optional[str] = None
    added_at: datetime
    category: Optional[str] = None  # <-- New

    class Config:
        orm_mode = True

class WishlistUpdate(BaseModel):
    book_name: str | None = None
    description: str | None = None
    category: str | None =None 
