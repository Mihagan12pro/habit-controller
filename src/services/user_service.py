from sqlalchemy import select
from sqlalchemy.orm import Session

from src import schemas
from src.models.user import User


def create_user(db: Session, user_dto: schemas.UserCreate):
    # Тут можно добавить хеширование пароля
    fake_hashed_pw = user_dto.password + "notreallyhashed"

    new_user = User(
        name=user_dto.name, email=user_dto.email, hashed_password=fake_hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(db: Session, email: str):
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_id(db: Session, user_id: int):
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()
