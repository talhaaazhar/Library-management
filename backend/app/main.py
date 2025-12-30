from fastapi import FastAPI
from fastapi import Depends
from app.api import auth
from app.middlewares.logging import LoggingMiddleware
from app.api.admin import (
    books as admin_books, 
    users as admin_user, 
    wishlist as admin_wishlist, 
    borrow as admin_borrow
) 
from app.api.user import books , user, wishlist, borrow

app = FastAPI()

# --------------------- MIDDLEWARE ---------------------
app.add_middleware(LoggingMiddleware)

app.include_router(auth.auth_router)
app.include_router(admin_books.Admin_books_router)
app.include_router(books.user_books_router)
app.include_router(admin_user.router)
app.include_router(user.router)
app.include_router(wishlist.router)
app.include_router(admin_wishlist.router)
app.include_router(borrow.router)
app.include_router(admin_borrow.router)

