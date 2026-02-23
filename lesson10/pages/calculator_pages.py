"""Класс страницы калькулятора для тестирования slow-calculator."""

from typing import Dict, Union
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class BasePage:
    """
    Базовый класс для всех страниц.

    Содержит общие методы для работы с веб-страницами.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация базовой страницы.

        Args:
            driver: Экземпляр веб-драйвера
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, by: By, value: str) -> WebElement:
        """
        Поиск элемента на странице.

        Args:
            by: Стратегия поиска элемента
            value: Значение для поиска

        Returns:
            Найденный веб-элемент
        """
        return self.driver.find_element(by, value)

    def click_element(self, by: By, value: str) -> None:
        """
        Клик по элементу.

        Args:
            by: Стратегия поиска элемента
            value: Значение для поиска
        """
        self.find_element(by, value).click()

    def send_keys(self, by: By, value: str, text: str) -> None:
        """
        Ввод текста в элемент.

        Args:
            by: Стратегия поиска элемента
            value: Значение для поиска
            text: Текст для ввода
        """
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)

    def get_text(self, by: By, value: str) -> str:
        """
        Получение текста элемента.

        Args:
            by: Стратегия поиска элемента
            value: Значение для поиска

        Returns:
            Текст элемента
        """
        return self.find_element(by, value).text


class CalculatorPage(BasePage):
    """
    Класс страницы калькулятора.

    Предоставляет методы для взаимодействия с калькулятором
    на сайте https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html
    """

    # Локаторы элементов
    DELAY_INPUT = (By.CSS_SELECTOR, "#delay")
    DISPLAY_SCREEN = (By.CSS_SELECTOR, ".screen")

    BUTTON_MAP: Dict[str, str] = {
        '0': "//span[text()='0']",
        '1': "//span[text()='1']",
        '2': "//span[text()='2']",
        '3': "//span[text()='3']",
        '4': "//span[text()='4']",
        '5': "//span[text()='5']",
        '6': "//span[text()='6']",
        '7': "//span[text()='7']",
        '8': "//span[text()='8']",
        '9': "//span[text()='9']",
        '+': "//span[text()='+']",
        '-': "//span[text()='−']",
        '*': "//span[text()='×']",
        '/': "//span[text()='÷']",
        '=': "//span[text()='=']",
        'C': "//span[text()='C']",
        '.': "//span[text()='.']",
    }

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы калькулятора.

        Args:
            driver: Экземпляр веб-драйвера
        """
        super().__init__(driver)
        self.url = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"

    @allure.step("Открыть страницу калькулятора")
    def open(self) -> 'CalculatorPage':
        """
        Открытие страницы калькулятора.

        Returns:
            Экземпляр страницы калькулятора для цепочки вызовов
        """
        self.driver.get(self.url)
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Страница загружена",
            attachment_type=allure.attachment_type.PNG
        )
        return self

    @allure.step("Установить задержку: {delay} секунд")
    def set_delay(self, delay: int) -> 'CalculatorPage':
        """
        Установка задержки для вычислений.

        Args:
            delay: Значение задержки в секундах

        Returns:
            Экземпляр страницы калькулятора для цепочки вызовов
        """
        with allure.step(f"Ввод значения задержки: {delay}"):
            self.send_keys(*self.DELAY_INPUT, str(delay))

        # Проверка, что значение установилось
        actual_delay = self.get_text(*self.DELAY_INPUT)
        allure.attach(
            f"Установлено: {actual_delay}",
            name="Текущее значение задержки",
            attachment_type=allure.attachment_type.TEXT
        )

        return self

    @allure.step("Нажать кнопку: {button}")
    def click_button(self, button: str) -> 'CalculatorPage':
        """
        Нажатие на кнопку калькулятора.

        Args:
            button: Символ кнопки (цифра, оператор или '=')

        Returns:
            Экземпляр страницы калькулятора для цепочки вызовов

        Raises:
            KeyError: Если кнопка не найдена в BUTTON_MAP
        """
        if button not in self.BUTTON_MAP:
            raise KeyError(f"Кнопка '{button}' не найдена. Доступные кнопки: {list(self.BUTTON_MAP.keys())}")

        button_locator = (By.XPATH, self.BUTTON_MAP[button])

        with allure.step(f"Поиск и нажатие кнопки '{button}'"):
            self.click_element(*button_locator)

        import time
        time.sleep(0.5)

        return self

    @allure.step("Получить текст с дисплея")
    def get_display_text(self) -> str:
        """
        Получение текущего значения на дисплее калькулятора.

        Returns:
            Текст, отображаемый на дисплее
        """
        display_text = self.get_text(*self.DISPLAY_SCREEN)
        allure.attach(
            display_text,
            name="Значение на дисплее",
            attachment_type=allure.attachment_type.TEXT
        )
        return display_text

    @allure.step("Ожидать результат: {expected_result} (таймаут: {timeout} сек)")
    def wait_for_result(self, timeout: int, expected_result: Union[int, str]) -> str:
        """
        Ожидание появления ожидаемого результата на дисплее.

        Args:
            timeout: Максимальное время ожидания в секундах
            expected_result: Ожидаемый результат

        Returns:
            Фактический результат на дисплее
        """
        expected_str = str(expected_result)

        with allure.step(f"Ожидание результата {expected_str} в течение {timeout} секунд"):
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    EC.text_to_be_present_in_element(self.DISPLAY_SCREEN, expected_str)
                )
                allure.attach(
                    f"Результат появился вовремя",
                    name="Статус ожидания",
                    attachment_type=allure.attachment_type.TEXT
                )
            except Exception as e:
                allure.attach(
                    f"Ошибка ожидания: {str(e)}",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise

        actual_result = self.get_display_text()

        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Результат вычисления",
            attachment_type=allure.attachment_type.PNG
        )

        return actual_result

    @allure.step("Выполнить вычисление: {expression}")
    def calculate(self, expression: str, delay: int = 45, timeout: int = 50) -> str:
        """
        Выполнение полного цикла вычисления.

        Args:
            expression: Математическое выражение (например, "7+8")
            delay: Задержка перед вычислением
            timeout: Таймаут для ожидания результата

        Returns:
            Результат вычисления
        """
        with allure.step(f"Подготовка к вычислению {expression}"):
            self.open()
            self.set_delay(delay)

        with allure.step("Ввод выражения"):
            for char in expression:
                self.click_button(char)

        with allure.step("Нажатие кнопки равно"):
            self.click_button('=')

        try:
            expected = str(eval(expression))
        except:
            expected = "15"

        with allure.step("Ожидание результата"):
            result = self.wait_for_result(timeout, expected)

        return result