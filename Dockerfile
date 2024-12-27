# Используем Python-образ в качестве базового
FROM python:3.11-slim

# Устанавливаем переменную окружения для отключения буферизации в Python
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения в контейнер
COPY . /app/

# Открываем порт, на котором будет работать Flask-приложение
EXPOSE 5000

# Команда для запуска Flask-приложения
CMD ["python", "app.py"]
