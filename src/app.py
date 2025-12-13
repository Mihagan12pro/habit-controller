from fastapi import FastAPI
from src.database import engine, Base
from src.routers import user, habit

# Создаем таблицы при старте
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flawless App API")

# Подключаем роутеры
app.include_router(user.router)
app.include_router(habit.router)

@app.get("/")
def root():
    return {"message": "Flawless API is running!"}