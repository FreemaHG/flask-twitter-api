FROM python:3.11

# Создаем директорию fastapi_app внутри контейнера
RUN mkdir /app

# Устанавливаем директорию app в качесте рабочей (переходим в нее)
WORKDIR /app

COPY app/requirements requirements
RUN pip install -r requirements/development.txt

# После копируем все остальные файлы (чаще изменяемые) внутрь рабочей директории
COPY app/ .
COPY docker/ docker
COPY .env .

# Данной командой мы разрешаем Docker выполнять все команды в папке docker с расширением .sh (bash-команды),
# которые в нашем случае используются для запуска Celery и Flower (в docker-compose.yml)
RUN chmod a+x docker/*.sh