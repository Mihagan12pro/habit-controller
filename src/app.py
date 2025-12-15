from fastapi import FastAPI

from src.database import engine
from src.routers.users import router as users_router
from src.routers.habits import router as habits_router
from src.models.base import Base

# Создаем таблицы при старте
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flawless App API")

# Подключаем роутеры
app.include_router(users_router)
app.include_router(habits_router)


@app.get("/")
def root():
    return {"message": "Flawless API is running!"}
