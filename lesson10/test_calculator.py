"""Тесты для проверки функциональности калькулятора."""

import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest

from pages.calculator_pages import CalculatorPage

@allure.feature("Калькулятор")
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("Slow Calculator Tests")
class TestCalculator:
    """Тестовый класс для проверки калькулятора."""

    def setup_method(self) -> None:
        """Настройка перед каждым тестом."""
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

    def teardown_method(self) -> None:
        """Очистка после каждого теста."""
        if self.driver:
            self.driver.quit()

    @allure.title("Проверка сложения с задержкой")
    @allure.description("Тест проверяет корректность сложения двух чисел с учетом установленной задержки")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "regression", "calculator")
    @allure.link("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html", name="Slow Calculator")
    @pytest.mark.parametrize("expression,expected,delay,timeout", [
        ("7+8", "15", 45, 50),
        ("5+3", "8", 30, 35),
        ("10+20", "30", 20, 25),
    ])
    def test_calculator_addition(self, expression: str, expected: str, delay: int, timeout: int) -> None:
        """
        Тест проверки сложения на калькуляторе.

        Args:
            expression: Выражение для вычисления
            expected: Ожидаемый результат
            delay: Задержка перед вычислением
            timeout: Таймаут для ожидания

        Шаги:
        1. Открыть страницу калькулятора
        2. Установить задержку
        3. Ввести выражение
        4. Нажать кнопку '='
        5. Дождаться результата
        6. Проверить соответствие ожидаемому
        """
        with allure.step(f"Инициализация страницы калькулятора"):
            calculator_page = CalculatorPage(self.driver)

        with allure.step(f"Выполнение вычисления {expression} с задержкой {delay}с"):
            result = calculator_page.calculate(expression, delay, timeout)

        with allure.step(f"Проверка результата"):
            allure.attach(
                f"Ожидалось: {expected}, Получено: {result}",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT
            )
            assert result == expected, f"Ожидалось '{expected}', получено '{result}'"

        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Финальный экран",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.title("Проверка базовых операций калькулятора")
    @allure.description("Тест проверяет работу всех основных операций калькулятора")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "calculator")
    @pytest.mark.parametrize("expression,expected", [
        ("7+8", "15"),
        ("10-3", "7"),
        ("5×6", "30"),
        ("20÷4", "5"),
    ])
    def test_calculator_operations(self, expression: str, expected: str) -> None:
        """
        Тест проверки различных операций калькулятора.

        Args:
            expression: Выражение для вычисления
            expected: Ожидаемый результат
        """
        calculator_page = CalculatorPage(self.driver)

        with allure.step(f"Тестирование выражения: {expression}"):
            calculator_page.open()
            calculator_page.set_delay(10)  # Маленькая задержка для быстрого теста

            # Ввод выражения
            for char in expression:
                calculator_page.click_button(char)

            calculator_page.click_button('=')

            # Ожидание результата
            result = calculator_page.wait_for_result(15, expected)

            with allure.step(f"Проверка результата"):
                assert result == expected, f"Для '{expression}' ожидалось '{expected}', получено '{result}'"

    @allure.title("Проверка обработки десятичных чисел")
    @allure.description("Тест проверяет работу калькулятора с десятичными дробями")
    @allure.severity(allure.severity_level.NORMAL)
    def test_calculator_decimal(self) -> None:
        """Тест проверки работы с десятичными числами."""
        calculator_page = CalculatorPage(self.driver)

        with allure.step("Вычисление 5.5 + 4.5"):
            calculator_page.open()
            calculator_page.set_delay(10)

            calculator_page.click_button('5')
            calculator_page.click_button('.')
            calculator_page.click_button('5')
            calculator_page.click_button('+')
            calculator_page.click_button('4')
            calculator_page.click_button('.')
            calculator_page.click_button('5')
            calculator_page.click_button('=')

            result = calculator_page.wait_for_result(15, "10")

            with allure.step("Проверка результата"):
                assert result == "10", f"Ожидалось '10', получено '{result}'"
                allure.attach(
                    f"5.5 + 4.5 = {result}",
                    name="Десятичное сложение",
                    attachment_type=allure.attachment_type.TEXT
                )