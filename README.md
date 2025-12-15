# Flawless Habit Tracker API

REST API на FastAPI для трекера привычек. Основные сущности: User, Habit, Progress.

## Стек технологий
Python 3.10+, FastAPI, SQLAlchemy, Pydantic, SQLite.

## Структура проекта
```
flawback/
├─ requirements.txt
├─ run_windows.bat
├─ run_mac.sh
├─ habitsController.db
└─ src/
   ├─ app.py
   ├─ database.py
   ├─ depends.py
   ├─ schemas.py
   ├─ models/
   │  ├─ base.py
   │  ├─ habit.py
   │  ├─ progress.py
   │  └─ user.py
   ├─ repositories/
   │  ├─ base.py
   │  ├─ habits.py
   │  ├─ progress.py
   │  └─ users.py
   ├─ routers/
   │  ├─ habits.py
   │  └─ users.py
   └─ services/
      ├─ habit_service.py
      ├─ progress_service.py
      └─ user_service.py
```

- `models` — ORM‑модели базы данных.
- `schemas.py` — Pydantic‑схемы (DTO) для валидации/сериализации.
- `repositories` — слой работы с БД (CRUD, транзакции).
- `services` — бизнес‑логика поверх репозиториев.
- `routers` — HTTP‑контроллеры (эндпоинты FastAPI).

## Установка и запуск

### Вариант A: быстрый запуск (скрипты)
- Windows: `run_windows.bat` (можете переименовать/создать алиас `run.bat`). Скрипт сам поднимет venv, поставит зависимости и запустит сервер.
- macOS/Linux: `chmod +x run_mac.sh && ./run_mac.sh`.

### Вариант B: ручная установка (консоль)
Выполняйте команды из корня проекта:
```bash
python -m venv venv
# Активировать окружение:
#   Windows: venv\Scripts\activate
#   macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn src.app:app --reload
```

## API и интеграция (для фронтенда)
- Актуальный билд лежит по ссылке: https://habit-controller.onrender.com/docs
- Документация и интерактивное тестирование: http://127.0.0.1:8000/docs
- Возможности: регистрация/логин, CRUD привычек, трекинг прогресса, получение статистики.
- Формат данных: JSON; даты передаются строками в формате `YYYY-MM-DD`.

## База данных
Используется SQLite. Файл `habitsController.db` создается автоматически в корне при первом запуске.

