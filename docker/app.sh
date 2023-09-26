#!/bin/bash

# Применяем миграции (создаем таблицы в БД)
#flask db upgrade

# Создание БД и наполнение демонстрационными данными
#python3 -m app.utils.data_migrations


# Запуск сервера
# TODO Автоматически создается БД
flask run