import json
import allure
import httpx
import pytest
from jsonschema import validate
from core.contracts import REGISTERED_USER_SCHEMA, LOGGED_IN_USER_SCHEMA



API_KEY = {"x-api-key": "reqres-free-v1"}  # Ключ API для того чтобы запросы не падали с 401 ошибкой.
BASE_URL = "https://reqres.in/api"
REGISTER_USER = "/register"
LOGIN_IN_USER = "/login"
users_data = json.load(open("core/new_users_data.json"))

@allure.suite("Регистрация пользователя")
class TestRegisterUser:
    @allure.title("Успешная регистрация пользователя (POST)")
    @pytest.mark.parametrize("user_data", users_data)
    def test_successful_register(self, user_data):
        with allure.step("Отправка POST запроса для регистрации нового пользователя"):
            response = httpx.post(url=BASE_URL + REGISTER_USER, json=user_data, headers=API_KEY)
            response_json = response.json()

        with allure.step("Проверка статус-кода ответ"):
            assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"

        with allure.step("Валидация успешной регистрации по JSON-схеме"):
            validate(response_json, REGISTERED_USER_SCHEMA)

    @allure.title("Негативные проверки регистрации (POST)")
    @pytest.mark.parametrize("user_data, expected_error", [
        ({"email": "eve.holt@reqres.in"}, "Missing password"),
        ({"password": "123321"}, "Missing email or username")
    ])
    def test_negative_register(self, user_data, expected_error):
        with allure.step(f"Отправка POST запроса с данными: {user_data}"):
            response = httpx.post(url=BASE_URL + REGISTER_USER, json=user_data, headers=API_KEY)
            response_json = response.json()

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 400, f"Ожидался 400, получили {response.status_code}"

        with allure.step("Проверка текста ошибки"):
            assert response_json["error"] == expected_error, f"Ожидали сообщение об ошибке: '{expected_error}', получили: '{response_json.get('error')}'"


@allure.suite("Авторизация пользователя")
class TestLoginUser:
    @allure.title("Успешная авторизация пользователя (POST)")
    @pytest.mark.parametrize("user_data", users_data)
    def test_successful_authorization(self, user_data):
        with allure.step("Отправка POST запроса для авторизации пользователя"):
            response = httpx.post(url=BASE_URL + LOGIN_IN_USER, json=user_data, headers=API_KEY)
            response_json = response.json()

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"


        with allure.step("Валидация успешной авторизации по JSON-схеме"):
            validate(response_json, LOGGED_IN_USER_SCHEMA)

    @allure.title("Негативные проверки авторизации (POST)")
    @pytest.mark.parametrize("user_data, expected_error", [
        ({"email": "eve.holt@reqres.in"}, "Missing password"),
        ({"password": "123321"}, "Missing email or username")
    ])
    def test_negative_authorization(self, user_data, expected_error):
        with allure.step(f"Отправка POST запроса с данными: {user_data}"):
            response = httpx.post(url=BASE_URL + LOGIN_IN_USER, json=user_data, headers=API_KEY)
            response_json = response.json()

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 400, f"Ожидался 400, получили {response.status_code}"

        with allure.step("Проверка текста ошибки"):
            assert response_json["error"] == expected_error, f"Ожидали сообщение об ошибке: '{expected_error}', получили: '{response_json.get('error')}'"