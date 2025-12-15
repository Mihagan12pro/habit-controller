@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ==========================================
echo       ЗАПУСК FLAWBACK (Smart Mode)
echo ==========================================

:: 1. Проверяем/Создаем venv
if not exist "venv" (
    echo [INFO] Создаю venv...
    python -m venv venv
)

:: 2. УМНАЯ ПРОВЕРКА ЗАВИСИМОСТЕЙ
set "REQ_FILE=requirements.txt"
set "MARKER_FILE=venv\requirements.last_install"

:: Если файла requirements вообще нет — ошибка
if not exist "%REQ_FILE%" (
    echo [ERROR] %REQ_FILE% не найден!
    pause
    exit /b
)

:: Проверяем: если нет маркерного файла -> надо ставить
if not exist "%MARKER_FILE%" goto :INSTALL_DEPS

:: Сравниваем текущий файл с тем, что был при последней установке
:: fc (file compare) вернет ошибку, если файлы разные
fc /b "%REQ_FILE%" "%MARKER_FILE%" >nul
if errorlevel 1 goto :INSTALL_DEPS

echo [INFO] Зависимости не менялись. Пропуск установки.
goto :START_SERVER

:INSTALL_DEPS
echo [INFO] Найдены изменения в requirements.txt (или первый запуск).
echo [INFO] Устанавливаю зависимости...
.\venv\Scripts\python.exe -m pip install -r requirements.txt

:: Если установка прошла успешно, обновляем маркерный файл (копируем текущий requirements внутрь venv)
if %errorlevel% equ 0 (
    copy /y "%REQ_FILE%" "%MARKER_FILE%" >nul
) else (
    echo [ERROR] Ошибка установки зависимостей!
    pause
    exit /b
)

:START_SERVER
:: 3. Открываем браузер и запускаем сервер
echo [INFO] Старт сервера...
timeout /t 2 /nobreak >nul
start http://127.0.0.1:8000/docs

.\venv\Scripts\uvicorn.exe src.app:app --reload
pause