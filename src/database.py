# src/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Меняем строку подключения. 
# "sqlite:///./flawless.db" означает, что файл создастся в текущей папке.
SQLALCHEMY_DATABASE_URL = "sqlite:///./flawless.db"

# 2. Создаем движок
# connect_args={"check_same_thread": False} — ЭТО ВАЖНО ТОЛЬКО ДЛЯ SQLITE
# (нужно, чтобы FastAPI мог работать с базой в многопоточном режиме)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()