import allure
import httpx
from jsonschema import validate
from core.contracts import UPDATED_USER_SCHEMA
import datetime
API_KEY = {"x-api-key": "reqres-free-v1"}  # Ключ API для того чтобы запросы не падали с 401 ошибкой.
BASE_URL = "https://reqres.in/api"
UPDATE_USER = "/users/2"


@allure.suite("Проверка обновления данных пользователя ")
class TestUpdateUserData:
    @allure.title("Обновление данных пользователя с полями name и job (PUT)")
    def test_update_user_with_name_and_job(self):
        with allure.step("Подготовка данных для обновления"):
            body = {
                "name": "morpheus",
                "job": "zion resident",
            }

        with allure.step("Отправка PUT запроса c новыми параметрами name и job"):
            response = httpx.put(url=BASE_URL + UPDATE_USER, json=body, headers=API_KEY)
            response_json = response.json()

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"

        with allure.step("Валидация данных пользователя по JSON-схеме"):
            validate(response_json, UPDATED_USER_SCHEMA)

        with (allure.step("Валидация значений полей в ответе")):
            update_date = response_json["updatedAt"].replace("T", " ")[0:16]
            current_date = str(datetime.datetime.now(datetime.timezone.utc))[0:16]
            assert update_date == current_date, f"Значения полей 'updatedAt' не совпадают."
            assert body["name"] == response_json["name"],f"Значения полей 'name' не совпадают. Ожидали {body['name']}, получили {response_json['name']}"
            assert body["job"] == response_json["job"], f"Значения полей 'job' не совпадают. Ожидали {body['job']}, получили {response_json['job']}"

    @allure.title("Обновление данных пользователя без поля job (PUT)")
    def test_update_user_without_job(self):
        with allure.step("Подготовка данных для обновления"):
            body = {
                "name": "morpheus"
            }

        with allure.step("Отправка PUT запроса c новым параметром name"):
            response = httpx.put(url=BASE_URL + UPDATE_USER, json=body, headers=API_KEY)
            response_json = response.json()

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"

        with allure.step("Валидация данных пользователя по JSON-схеме"):
            validate(response_json, UPDATED_USER_SCHEMA)

        with (allure.step("Валидация значений полей в ответе")):
            update_date = response_json["updatedAt"].replace("T", " ")[0:16]
            current_date = str(datetime.datetime.now(datetime.timezone.utc))[0:16]
            assert update_date == current_date, f"Значения полей 'updatedAt' не совпадают."
            assert body["name"] == response_json["name"],f"Значения полей 'name' не совпадают. Ожидали {body['name']}, получили {response_json['name']}"

    @allure.title("Обновление данных пользователя без поля name (PUT)")
    def test_update_user_without_name(self):
        with allure.step("Подготовка данных для обновления"):
            body = {
                "job": "zion resident"
            }

        with allure.step("Отправка PUT запроса c новым параметром job"):
            response = httpx.put(url=BASE_URL + UPDATE_USER, json=body, headers=API_KEY)
            response_json = response.json()

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"

        with allure.step("Валидация данных пользователя по JSON-схеме"):
            validate(response_json, UPDATED_USER_SCHEMA)

        with (allure.step("Валидация значений полей в ответе")):
            update_date = response_json["updatedAt"].replace("T", " ")[0:16]
            current_date = str(datetime.datetime.now(datetime.timezone.utc))[0:16]
            assert update_date == current_date, f"Значения полей 'updatedAt' не совпадают."
            assert body["job"] == response_json["job"], f"Значения полей 'job' не совпадают. Ожидали {body['job']}, получили {response_json['job']}"

    @allure.title("Обновление данных пользователя без тела (PUT)")
    def test_update_user_without_body(self):

        with allure.step("Отправка PUT запроса без тела"):
            response = httpx.put(url=BASE_URL + UPDATE_USER, headers=API_KEY)
            response_json = response.json()

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"

        with allure.step("Валидация данных пользователя по JSON-схеме"):
            validate(response_json, UPDATED_USER_SCHEMA)

        with (allure.step("Валидация значений полей в ответе")):
            update_date = response_json["updatedAt"].replace("T", " ")[0:16]
            current_date = str(datetime.datetime.now(datetime.timezone.utc))[0:16]
            assert update_date == current_date, f"Значения полей 'updatedAt' не совпадают."
            assert len(response_json) == 1, f"В ответ пришло больше чем одно значение (updatedAt)"

    @allure.title("Частичное обновление пользователя с параметром job (PATCH)")
    def test_patch_user_with_job_only(self):
        with allure.step("Подготовка данных для частичного обновления"):
            body = {
                "job": "matrix admin"
            }

        with allure.step("Отправка PATCH-запроса"):
            response = httpx.patch(url=BASE_URL + UPDATE_USER, json=body, headers=API_KEY)
            response_json = response.json()


        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"

        with allure.step("Валидация данных пользователя по JSON-схеме"):
            validate(response_json, UPDATED_USER_SCHEMA)

        with (allure.step("Валидация значений полей в ответе")):
            update_date = response_json["updatedAt"].replace("T", " ")[0:16]
            current_date = str(datetime.datetime.now(datetime.timezone.utc))[0:16]
            assert update_date == current_date, f"Значения полей 'updatedAt' не совпадают."
            assert body["job"] == response_json["job"], f"Значения полей 'job' не совпадают. Ожидали {body['job']}, получили {response_json['job']}"

    @allure.title("Обновление пользователя с пустым телом (PATCH)")
    def test_patch_user_without_body(self):
        with allure.step("Отправка PATCH-запроса без тела"):
            response = httpx.patch(url=BASE_URL + UPDATE_USER, headers=API_KEY)
            response_json = response.json()


        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"

        with allure.step("Валидация данных пользователя по JSON-схеме"):
            validate(response_json, UPDATED_USER_SCHEMA)

        with (allure.step("Валидация значений полей в ответе")):
            update_date = response_json["updatedAt"].replace("T", " ")[0:16]
            current_date = str(datetime.datetime.now(datetime.timezone.utc))[0:16]
            assert update_date == current_date, f"Значения полей 'updatedAt' не совпадают."
            assert len(response_json) == 1, f"В ответ пришло больше чем одно значение (updatedAt)"