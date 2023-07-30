import os
import shutil

from functools import wraps
from http import HTTPStatus
from pathlib import Path
from flask import current_app
from loguru import logger

from app.tests.conftest import app, client, db


TEST_ROOT_DIR = Path(__file__).resolve().parents[1]  # Корневая директория с тестами


def clear_path(func):
    """
    функция-декоратор для удаления созданных папок и файлов при тестировании загрузки изображений
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        func(*args, **kwargs)

        delete_path = os.path.join(TEST_ROOT_DIR, 'routes', 'static')

        try:
            shutil.rmtree(delete_path)
        except FileNotFoundError:
            logger.warning(f'Директория {delete_path} не найдена!')

    return decorator


@clear_path
def test_load_image(client) -> None:
    """
    Тестирование загрузки изображения к твиту
    """
    image_name = os.path.join(TEST_ROOT_DIR, 'files_for_tests', 'test_image.jpg')
    image = (open(image_name, 'rb'), 'test_image.jpg')

    resp = client.post(
        '/api/medias',
        data={'file': image},
        headers={'api-key': 'test-user1', 'Content-Type': 'multipart/form-data'}
    )

    await_response = {
        'result': True,
        'media_id': 3
    }

    assert resp.status_code == HTTPStatus.CREATED
    assert resp.json == await_response


def test_load_incorrect_file(client) -> None:
    """
    Тестирование вывода сообщения об ошибке при попытке загрузить файл неразрешенного формата
    """
    file_name = os.path.join(TEST_ROOT_DIR, 'files_for_tests', 'test_bad_file.txt')
    file = (open(file_name, 'rb'), 'test_bad_file.txt')

    resp = client.post(
        '/api/medias',
        data={'file': file},
        headers={'api-key': 'test-user1', 'Content-Type': 'multipart/form-data'}
    )

    allowed_format = ", ".join(
        elem for elem in current_app.config['ALLOWED_EXTENSIONS']
    )

    await_response = {
        'result': False,
        'error_type': f'{HTTPStatus.UNPROCESSABLE_ENTITY}',
        'error_message': f'Invalid images format. Only {allowed_format} files accepted'
    }

    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert resp.json == await_response
