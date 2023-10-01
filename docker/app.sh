#!/bin/bash

# Заполнить БД демонстрационными данными
python3 -m app.utils.data_migrations

# Запуск сервера
gunicorn app.main:app --bind=0.0.0.0:5000