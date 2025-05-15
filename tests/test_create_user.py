import allure
import httpx
from jsonschema import validate
from core.contracts import CREATED_USER_SCHEMA
import datetime
API_KEY = {"x-api-key": "reqres-free-v1"}  # Ключ API для того чтобы запросы не падали с 401 ошибкой.
BASE_URL = "https://reqres.in/api"
CREATE_USER = "/users"


@allure.suite("Проверка создания пользователя")
class TestCreateUser:
    @allure.title("Создание нового пользователя c параметрами name и job (POST)")
    def test_create_user_with_name_and_job(self):
        with allure.step("Подготовка данных для создания нового пользователя"):
            body = {
                "name": "morpheus",
                "job": "leader",
            }

        with allure.step("Отправка POST запроса c информацией о новом пользователе"):
            response = httpx.post(url=BASE_URL + CREATE_USER, json=body, headers=API_KEY)
            response_json = response.json()

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 201, f"Ожидался 201, получили {response.status_code}"

        with allure.step("Валидация данных пользователя по JSON-схеме"):
            validate(response_json, CREATED_USER_SCHEMA)

        with (allure.step("Валидация значений полей в ответе")):
            creation_date = response_json["createdAt"].replace("T", " ")[0:16]
            current_date = str(datetime.datetime.now(datetime.timezone.utc))[0:16]
            assert creation_date == current_date, f"Значения полей 'createdAt' не совпадают."
            assert body["name"] == response_json["name"],f"Значения полей 'name' не совпадают. Ожидали {body['name']}, получили {response_json['name']}"
            assert body["job"] == response_json["job"], f"Значения полей 'job' не совпадают. Ожидали {body['job']}, получили {response_json['job']}"

    @allure.title("Создание нового пользователя без параметра name (POST)")
    def test_create_user_without_name(self):
        with allure.step("Подготовка данных для создания нового пользователя"):
            body = {
                "job": "leader"
            }

        with allure.step("Отправка POST запроса c информацией о новом пользователе"):
            response = httpx.post(url=BASE_URL + CREATE_USER, json=body, headers=API_KEY)
            response_json = response.json()

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 201, f"Ожидался 201, получили {response.status_code}"

        with allure.step("Валидация данных пользователя по JSON-схеме"):
            validate(response_json, CREATED_USER_SCHEMA)

        with allure.step("Валидация значений полей в ответе"):
            creation_date = response_json["createdAt"].replace("T", " ")[0:16]
            current_date = str(datetime.datetime.now(datetime.timezone.utc))[0:16]
            assert creation_date == current_date, f"Значения полей 'createdAt' не совпадают."
            assert body["job"] == response_json["job"], f"Значения полей 'job' не совпадают. Ожидали {body['job']}, получили {response_json['job']}"

    @allure.title("Создание нового пользователя без параметра job (POST)")
    def test_create_user_without_job(self):
        with allure.step("Подготовка данных для создания нового пользователя"):
            body = {
                "name": "morpheus",
            }

        with allure.step("Отправка POST запроса c информацией о новом пользователе"):
            response = httpx.post(url=BASE_URL + CREATE_USER, json=body, headers=API_KEY)
            response_json = response.json()

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 201, f"Ожидался 201, получили {response.status_code}"

        with allure.step("Валидация данных пользователя по JSON-схеме"):
            validate(response_json, CREATED_USER_SCHEMA)

        with allure.step("Валидация значений полей в ответе"):
            creation_date = response_json["createdAt"].replace("T", " ")[0:16]
            current_date = str(datetime.datetime.now(datetime.timezone.utc))[0:16]
            assert creation_date == current_date, f"Значения полей 'createdAt' не совпадают."
            assert body["name"] == response_json["name"],f"Значения полей 'name' не совпадают. Ожидали {body['name']}, получили {response_json['name']}"


