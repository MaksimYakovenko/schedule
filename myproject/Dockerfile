# Базовый образ
FROM python:3.10-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем код
COPY . .

# Открываем порт (если нужно)
EXPOSE 8000

# Команда запуска
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
