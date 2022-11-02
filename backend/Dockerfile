FROM python:3.7-slim

WORKDIR /app
 
# Копируем файлы проекта в контейнер.
COPY backend/. .
# Выполняем установку зависимостей внутри контейнера.
# раскоментировать что бы собрать на маке
# RUN apt-get update \
#    && apt-get -y install libpq-dev gcc
RUN python3 -m pip install --upgrade pip setuptools
RUN pip3 install -r /app/requirements.txt --no-cache-dir

# Выполнить запуск сервера при старте контейнера. 
# Для отображения отладочной информации добавить ключ "--log-syslog"
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]
