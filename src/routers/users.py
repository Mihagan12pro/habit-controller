from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import schemas
from src.database import get_db
from src.services.user_service import create_user, get_user_by_email

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверяем, занят ли email
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    return create_user(db, user)
