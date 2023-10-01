FROM python:3.11

COPY requirements/base.txt /app/requirements/base.txt
COPY requirements/production.txt /app/requirements/production.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements/production.txt

COPY ./app /app

COPY ./docker /docker

# Разрешаем Docker выполнять команды в ./docker/<file>.sh (bash-команды),
# используемые для загрузки демонстрационных данных и запуска сервера
RUN chmod a+x docker/*.sh

# gunicorn
# Обязательно указываем порт, иначе приложение из контейнера не будет отправлять ответ за пределы контейнера
#CMD gunicorn app.main:app --bind=0.0.0.0:5000