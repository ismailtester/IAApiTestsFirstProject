import allure
import httpx
from jsonschema import validate

from core.contracts import USER_DATA_SCHEMA

BASE_URL = "https://reqres.in/api"
API_KEY = {"x-api-key": "reqres-free-v1"}  # Ключ API для того чтобы запросы не падали с 401 ошибкой.
LIST_USERS = "/users?page=2"
DELAYED_USERS_LIST = "/users?delay=3"
EMAIL_ENDS = "@reqres.in"
AVATAR_ENDS = f"-image.jpg"
SINGLE_USER = "/users/2"
NOT_FOUND_USER = "/users/23"


@allure.suite("Проверка запросов данных пользователей")
class TestUserData:
    @allure.title("Получение списка пользователей (GET)")
    def test_get_list_users(self):
        with allure.step(f"Отправка GET запроса для получения списка пользователей по URL: {BASE_URL + LIST_USERS}"):
            response = httpx.get(BASE_URL + LIST_USERS, headers=API_KEY)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"

        data = response.json()["data"]
        for item in data:
            with allure.step("Проверка данных пользователей по JSON-схеме"):
                validate(item, USER_DATA_SCHEMA)
                with allure.step("Проверка окончания email-адреса"):
                    assert item["email"].endswith(EMAIL_ENDS), f"Email пользователя должен заканчиваться на {EMAIL_ENDS}"
                with allure.step("Проверка наличия ID в URL аватара"):
                    assert item["avatar"].endswith(str(item["id"]) + AVATAR_ENDS), f"Ссылка на аватар пользователя должна содержать ID и заканчиваться на {AVATAR_ENDS}"

    @allure.title("Получение информации об одном пользователе (GET)")
    def test_get_single_user(self):
        with allure.step("Отправка GET запроса на получение данных пользователя"):
            response = httpx.get(BASE_URL + SINGLE_USER, headers=API_KEY)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"
        data = response.json()["data"]
        with allure.step("Валидация данных пользователя по JSON-схеме"):
            validate(data, USER_DATA_SCHEMA)
            with allure.step("Проверка окончания email-адреса"):
                assert data["email"].endswith(EMAIL_ENDS), f"Отсутствует reqres.in в конце email"
            with allure.step("Проверка наличия ID в URL аватара"):
                assert data["avatar"].endswith(str(data["id"]) + AVATAR_ENDS), f"В ссылке на аватарку, отсутствует ID пользователя"

    @allure.title("Получение несуществующего пользователя — ожидаем 404 (GET)")
    def test_get_user_not_found(self):
        with allure.step("Отправка GET запроса на несуществующего пользователя"):
            response = httpx.get(BASE_URL + NOT_FOUND_USER, headers=API_KEY)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 404, f"Ожидался 404, получили {response.status_code}"

    @allure.title("Получение списка пользователей c задержкой (GET)")
    def test_get_delayed_user_list(self):
        with allure.step(f"Отправка GET запроса для получения списка пользователей по URL: {BASE_URL + DELAYED_USERS_LIST}"):
            response = httpx.get(BASE_URL + DELAYED_USERS_LIST, headers=API_KEY, timeout=4)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"

        data = response.json()["data"]
        for item in data:
            with allure.step("Проверка данных пользователей по JSON-схеме"):
                validate(item, USER_DATA_SCHEMA)
                with allure.step("Проверка окончания email-адреса"):
                    assert item["email"].endswith(EMAIL_ENDS), f"Email пользователя должен заканчиваться на {EMAIL_ENDS}"
                with allure.step("Проверка наличия ID в URL аватара"):
                    assert item["avatar"].endswith(str(item["id"]) + AVATAR_ENDS), f"Ссылка на аватар пользователя должна содержать ID и заканчиваться на {AVATAR_ENDS}"

