#!/bin/bash

# 1. Переходим в директорию скрипта
cd "$(dirname "$0")"

echo "=========================================="
echo "       ЗАПУСК FLAWBACK (MacOS Smart)"
echo "=========================================="

# 2. Проверяем/Создаем venv
if [ ! -d "venv" ]; then
    echo "[INFO] Создаю venv..."
    python3 -m venv venv
fi

# Активируем окружение
source venv/bin/activate

# 3. УМНАЯ ПРОВЕРКА ЗАВИСИМОСТЕЙ
REQ_FILE="requirements.txt"
MARKER_FILE="venv/requirements.last_install"

# Если файла вообще нет
if [ ! -f "$REQ_FILE" ]; then
    echo "[ERROR] $REQ_FILE не найден!"
    exit 1
fi

# Функция установки
install_deps() {
    echo "[INFO] Устанавливаю зависимости..."
    pip install -r "$REQ_FILE"
    
    # Если успешно, копируем файл как маркер
    if [ $? -eq 0 ]; then
        cp "$REQ_FILE" "$MARKER_FILE"
    else
        echo "[ERROR] Ошибка установки!"
        exit 1
    fi
}

# Логика сравнения
if [ ! -f "$MARKER_FILE" ]; then
    # Если маркера нет (первый запуск) -> ставим
    echo "[INFO] Первый запуск или маркер отсутствует."
    install_deps
else
    # Сравниваем файлы (cmp -s работает молча)
    if cmp -s "$REQ_FILE" "$MARKER_FILE"; then
        echo "[INFO] Зависимости не менялись. Пропуск установки."
    else
        echo "[INFO] Найдены изменения в requirements.txt."
        install_deps
    fi
fi

# 4. Запуск
echo "[INFO] Старт сервера..."
# Запускаем открытие браузера в фоне
(sleep 2 && open http://127.0.0.1:8000/docs) &

# Запускаем uvicorn
uvicorn src.app:app --reload