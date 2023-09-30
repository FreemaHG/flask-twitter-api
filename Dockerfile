FROM python:3.11

COPY requirements/base.txt /app/requirements/base.txt
COPY requirements/production.txt /app/requirements/production.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements/production.txt

COPY ./app /app

# gunicorn
# Обязательно указываем порт, иначе приложение из контейнера не будет отправлять ответ за пределы контейнера
CMD gunicorn app.main:app --workers 4 --bind=0.0.0.0:5000