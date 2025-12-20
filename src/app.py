from fastapi import FastAPI

from src.database import engine
from src.routers.users import router as users_router
from src.routers.habits import router as habits_router
from src.models.base import Base


async def init_db():
    """Инициализация базы данных - создание таблиц"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(title="Flawless App API", on_startup=[init_db])

# Подключаем роутеры
app.include_router(users_router)
app.include_router(habits_router)


@app.get("/")
async def root():
    return {"message": "Flawless API is running!"}
