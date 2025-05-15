import allure
import httpx
from jsonschema import validate
from core.contracts import CREATED_USER_SCHEMA
API_KEY = {"x-api-key": "reqres-free-v1"}  # Ключ API для того чтобы запросы не падали с 401 ошибкой.
BASE_URL = "https://reqres.in/api"
DELETE_USER = "/users/2"


"""В этом сьюте только один тест, по той простой причине что в данный момент апи reqres.in на любой айдишник отдает 204, и по сути нет несуществующего пользователя"""
@allure.suite("Проверка удаления пользователя")
class TestDeleteUser:
    @allure.title("Удаление существующего пользователя")
    def test_delete_existing_user(self):
        with allure.step("Отправка DELETE запроса"):
            response = httpx.delete(url=BASE_URL + DELETE_USER, headers=API_KEY)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 204, f"Ожидался 204, получили {response.status_code}"
