import os
import shutil

from functools import wraps
from http import HTTPStatus
from pathlib import Path

import pytest
from flask import current_app
from loguru import logger


TEST_ROOT_DIR = Path(__file__).resolve().parents[1]  # Корневая директория с тестами

class TestImages:

    @pytest.fixture
    def image(self):
        image_name = os.path.join(TEST_ROOT_DIR, 'files_for_tests', 'test_image.jpg')
        image = (open(image_name, 'rb'), 'test_image.jpg')
        return image

    @pytest.fixture
    def incorrect_file(self):
        file_name = os.path.join(TEST_ROOT_DIR, 'files_for_tests', 'test_bad_file.txt')
        file = (open(file_name, 'rb'), 'test_bad_file.txt')
        return file

    def send_request(self, client, file):
        resp = client.post(
            '/api/medias',
            data={'file': file},
            headers={'api-key': 'test-user1', 'Content-Type': 'multipart/form-data'}
        )

        return resp

    def clear_path(func):
        """
        Декоратор для удаления созданных папок и файлов при тестировании загрузки изображений
        """
        @wraps(func)
        def decorator(*args, **kwargs):
            func(*args, **kwargs)
            delete_path = os.path.join(TEST_ROOT_DIR, 'static')

            print(f'Удаление директории: {delete_path}')
            logger.info(f'Удаление директории: {delete_path}')

            try:
                shutil.rmtree(delete_path)
            except FileNotFoundError:
                logger.warning(f'Директория {delete_path} не найдена!')

        return decorator


    @clear_path
    def test_load_image(self, client, users, image, good_response) -> None:
        """
        Тестирование загрузки изображения к твиту
        """
        resp = self.send_request(client=client, file=image)
        good_response['media_id'] = 1

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert resp.json == good_response


    def test_load_incorrect_file(self, client, users, incorrect_file, bad_response) -> None:
        """
        Тестирование вывода сообщения об ошибке при попытке загрузить файл неразрешенного формата
        """
        resp = self.send_request(client=client, file=incorrect_file)

        allowed_format = ", ".join(
            elem for elem in current_app.config['ALLOWED_EXTENSIONS']
        )

        bad_response['error_type'] = f'{HTTPStatus.UNPROCESSABLE_ENTITY}'
        bad_response['error_message'] = f'Invalid images format. Only {allowed_format} files accepted'

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert resp.json == bad_response
