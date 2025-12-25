import asyncio
import sys
from contextlib import asynccontextmanager

# --- ФИКС ДЛЯ WINDOWS (Обязательно вставить это) ---
# Это решает проблему "ломающейся консоли" и зависания при перезагрузке
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI

from src.database import engine
from src.models.base import Base
from src.routers.cessation import router as cessation_router
from src.routers.habit import router as habit_router
from src.routers.user import router as user_router


# --- ИСПОЛЬЗУЕМ LIFESPAN ВМЕСТО ON_STARTUP ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Блок запуска: создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # Тут приложение работает

    # Блок выключения: корректно закрываем соединение с БД!
    # Это ключевой момент, чтобы релоад не вешал сервер
    await engine.dispose()


# Передаем lifespan в FastAPI
app = FastAPI(title="Flawless App API", lifespan=lifespan)

# Подключаем роутеры
app.include_router(user_router)
app.include_router(habit_router)
app.include_router(cessation_router)


@app.get("/")
async def root():
    return {"message": "Flawless API is running!"}
