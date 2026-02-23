"""Тесты для проверки функциональности SauceDemo."""

import allure
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pages.all_pages import LoginPage


@allure.feature("Оформление заказа")
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("SauceDemo Tests")
class TestSauceDemo:
    """Тестовый класс для проверки оформления заказа."""

    def setup_method(self) -> None:
        """Настройка перед каждым тестом."""
        options = Options()
        options.add_argument("--headless")  # Запуск в фоновом режиме для CI/CD
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def teardown_method(self) -> None:
        """Очистка после каждого теста."""
        if self.driver:
            self.driver.quit()

    @allure.title("Проверка итоговой суммы заказа")
    @allure.description("Тест проверяет корректность расчета итоговой суммы при добавлении товаров в корзину")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "regression", "ui")
    @allure.link("https://www.saucedemo.com", name="SauceDemo")
    def test_total_price(self) -> None:
        """
        Тест проверки итоговой суммы заказа.

        Шаги:
        1. Открыть страницу авторизации
        2. Выполнить вход с валидными учетными данными
        3. Добавить товары в корзину
        4. Перейти в корзину
        5. Перейти к оформлению заказа
        6. Заполнить форму с персональными данными
        7. Получить итоговую сумму
        8. Проверить соответствие ожидаемой сумме
        """
        expected_total = "Total: $58.29"

        with allure.step("Инициализация страницы авторизации"):
            login_page = LoginPage(self.driver)

        with allure.step("Выполнение авторизации"):
            inventory_page = login_page.open().login("standard_user", "secret_sauce")

        with allure.step("Добавление товаров в корзину"):
            inventory_page.add_items()

        with allure.step("Переход в корзину"):
            cart_page = inventory_page.go_to_cart()

        with allure.step("Начало оформления заказа"):
            checkout_page = cart_page.checkout()

        with allure.step("Заполнение персональных данных"):
            checkout_page.fill_form("Aytalina", "Ivanova", "123456")

        with allure.step("Получение итоговой суммы"):
            actual_total = checkout_page.get_total()
            allure.attach(
                f"Ожидалось: {expected_total}, Получено: {actual_total}",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Проверка итоговой суммы"):
            assert actual_total == expected_total, \
                f"Ожидалось '{expected_total}', получено '{actual_total}'"

        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Финальный экран",
            attachment_type=allure.attachment_type.PNG
        )