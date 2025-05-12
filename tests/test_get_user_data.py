import allure
import httpx
from jsonschema import validate

from core.contracts import USER_DATA_SCHEMA

BASE_URL = "https://reqres.in/api"
API_KEY = {"x-api-key": "reqres-free-v1"}  # Ключ API для того чтобы запросы не падали с 401 ошибкой.
LIST_USERS = "/users?page=2"
EMAIL_ENDS = "@reqres.in"
AVATAR_ENDS = f"-image.jpg"
SINGLE_USER = "/users/2"
NOT_FOUND_USER = "/users/23"

class TestUserData:
    @allure.title("Получение списка пользователей")
    def test_get_list_users(self):
        with allure.step("Отправка запроса для получения списка пользователей"):
            response = httpx.get(BASE_URL + LIST_USERS, headers=API_KEY)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Неверный статус код"

        with allure.step("Валидация данных пользователей"):
            data = response.json()["data"]
            for item in data:
                validate(item, USER_DATA_SCHEMA)
                assert item["email"].endswith(EMAIL_ENDS), f"Email пользователя должен заканчиваться на {EMAIL_ENDS}"
                assert item["avatar"].endswith(str(item["id"]) + AVATAR_ENDS), f"Ссылка на аватар пользователя должна содержать ID и заканчиваться на {AVATAR_ENDS}"

    @allure.title("Получение информации об одном пользователе")
    def test_get_single_user(self):
        with allure.step("Отправка запроса для получения данных об одном пользователе"):
            response = httpx.get(BASE_URL + SINGLE_USER, headers=API_KEY)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Неверный статус код"

        with allure.step("Валидация данных пользователя"):
            data = response.json()["data"]
            assert data["email"].endswith(EMAIL_ENDS), f"Отсутствует reqres.in в конце email"
            assert data["avatar"].endswith(str(data["id"]) + AVATAR_ENDS), f"В ссылке на аватарку, отсутствует ID пользователя"

    @allure.title("Попытка получить информацию о несуществующем пользователе")
    def test_get_user_not_found(self):
        with allure.step("Отправка запроса для получения данных несуществующего пользователя"):
            response = httpx.get(BASE_URL + NOT_FOUND_USER, headers=API_KEY)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, f"Неверный статус код"
