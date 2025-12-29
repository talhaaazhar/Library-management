"""Create a single admin user (safe to run directly).

This script ensures the project root is on `sys.path` so it can be
executed with `python app/admin.py` from the `backend` folder.
"""
import os
import sys

# ensure project root (backend/) is on sys.path when running as a script
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.core.database import SessionLocal
from app.models import User
from app.core.security import hash_password


def main():
    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.role == "admin").first()
        if existing_admin:
            print("Admin user already exists.")
            return

        admin_user = User(
            name="Super Admin",
            email="admin@gmail.com",
            password=hash_password("12345678"),
            role="admin",
            is_active=True,
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print(f"Admin user created: {admin_user.email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
