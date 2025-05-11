import allure
import httpx
from jsonschema import validate

from core.contracts import RESOURCE_DATA_SCHEMA

BASE_URL = "https://reqres.in/api"
API_KEY = {"x-api-key": "reqres-free-v1"}  # Ключ API для того чтобы запросы не падали с 401 ошибкой.
LIST_RESOURCE = "/unknown"
SINGLE_RESOURCE = "/unknown/2"
NOT_FOUND_RESOURCE = "/unknown/23"

@allure.suite("Проверка запросов данных ресурсов")
class TestResourceData:
    @allure.title("Получение списка ресурсов")
    def test_get_list_resource(self):
        with allure.step("Отправка запроса на получение списка ресурсов"):
            response = httpx.get(BASE_URL + LIST_RESOURCE, headers=API_KEY)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"

        data = response.json()["data"]
        for item in data:
            with allure.step("Проверка элементов списка по JSON-схеме"):
                validate(item, RESOURCE_DATA_SCHEMA)
                with allure.step("Проверка префикса «#» в поле color"):
                    assert item["color"].startswith("#"), f"Отсутствует префикс # у цветового кода"

    @allure.title("Получение информации об одном ресурсе")
    def test_get_single_resource(self):
        with allure.step("Отправка запроса на получение одного ресурса"):
            response = httpx.get(BASE_URL + SINGLE_RESOURCE, headers=API_KEY)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"

        with allure.step("Валидация данных ресурса по JSON-схеме"):
            data = response.json()["data"]
            validate(data, RESOURCE_DATA_SCHEMA)
            with allure.step("Проверка префикса «#» в поле color"):
                assert data["color"].startswith("#"), f"Отсутствует префикс # у цветового кода"

    @allure.title("Получение несуществующего ресурса — ожидаем 404")
    def test_get_resource_not_found(self):
        with allure.step("Отправка запроса на несуществующий ресурс"):
            response = httpx.get(BASE_URL + NOT_FOUND_RESOURCE, headers=API_KEY)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 404, f"Ожидался 404, получили {response.status_code}"
