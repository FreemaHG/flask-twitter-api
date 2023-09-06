#!/bin/bash

# Применяем миграции (создаем таблицы в БД)
flask db upgrade

# Запуск сервера
flask run