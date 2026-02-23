"""Все классы страниц для тестирования SauceDemo."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class BasePage:
    """
    Базовый класс для всех страниц.

    Содержит общие методы и атрибуты для работы с веб-страницами.
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
        Поиск элемента на странице с ожиданием.

        Args:
            by: Стратегия поиска элемента
            value: Значение для поиска

        Returns:
            Найденный веб-элемент
        """
        return self.wait.until(
            EC.presence_of_element_located((by, value))
        )

    def click_element(self, by: By, value: str) -> None:
        """
        Клик по элементу с ожиданием.

        Args:
            by: Стратегия поиска элемента
            value: Значение для поиска
        """
        element = self.wait.until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()

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
        element = self.find_element(by, value)
        return element.text


class LoginPage(BasePage):
    """
    Класс страницы авторизации.

    Предоставляет методы для взаимодействия со страницей входа.
    """

    # Локаторы элементов на странице
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы авторизации.

        Args:
            driver: Экземпляр веб-драйвера
        """
        super().__init__(driver)

    @allure.step("Открыть страницу авторизации")
    def open(self) -> 'LoginPage':
        """
        Открытие страницы авторизации.

        Returns:
            Экземпляр страницы авторизации для цепочки вызовов
        """
        self.driver.get("https://www.saucedemo.com/")
        return self

    @allure.step("Выполнить вход с логином {username} и паролем {password}")
    def login(self, username: str, password: str) -> 'InventoryPage':
        """
        Выполнение входа в систему.

        Args:
            username: Имя пользователя
            password: Пароль

        Returns:
            Экземпляр страницы с товарами
        """
        with allure.step(f"Ввод логина: {username}"):
            self.send_keys(*self.USERNAME_INPUT, username)

        with allure.step(f"Ввод пароля: {password}"):
            self.send_keys(*self.PASSWORD_INPUT, password)

        with allure.step("Нажатие кнопки входа"):
            self.click_element(*self.LOGIN_BUTTON)

        return InventoryPage(self.driver)


class InventoryPage(BasePage):
    """
    Класс страницы с товарами.

    Предоставляет методы для работы со списком товаров.
    """

    # Локаторы элементов
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    ADD_BOLT_T_SHIRT = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    ADD_ONESIE = (By.ID, "add-to-cart-sauce-labs-onesie")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы товаров.

        Args:
            driver: Экземпляр веб-драйвера
        """
        super().__init__(driver)

    @allure.step("Добавить выбранные товары в корзину")
    def add_items(self) -> 'InventoryPage':
        """
        Добавление товаров в корзину.

        Returns:
            Экземпляр страницы товаров для цепочки вызовов
        """
        items = [
            ("Sauce Labs Backpack", self.ADD_BACKPACK),
            ("Sauce Labs Bolt T-Shirt", self.ADD_BOLT_T_SHIRT),
            ("Sauce Labs Onesie", self.ADD_ONESIE)
        ]

        for item_name, locator in items:
            with allure.step(f"Добавление товара: {item_name}"):
                self.click_element(*locator)

        return self

    @allure.step("Перейти в корзину")
    def go_to_cart(self) -> 'CartPage':
        """
        Переход на страницу корзины.

        Returns:
            Экземпляр страницы корзины
        """
        with allure.step("Нажатие на иконку корзины"):
            self.click_element(*self.CART_LINK)

        return CartPage(self.driver)


class CartPage(BasePage):
    """
    Класс страницы корзины.

    Предоставляет методы для работы с корзиной покупок.
    """

    # Локаторы элементов
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы корзины.

        Args:
            driver: Экземпляр веб-драйвера
        """
        super().__init__(driver)

    @allure.step("Перейти к оформлению заказа")
    def checkout(self) -> 'CheckoutPage':
        """
        Начало оформления заказа.

        Returns:
            Экземпляр страницы оформления заказа
        """
        with allure.step("Нажатие кнопки 'Checkout'"):
            self.click_element(*self.CHECKOUT_BUTTON)

        return CheckoutPage(self.driver)


class CheckoutPage(BasePage):
    """
    Класс страницы оформления заказа.

    Предоставляет методы для заполнения формы заказа
    и получения итоговой суммы.
    """

    # Локаторы элементов
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    ZIP_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы оформления заказа.

        Args:
            driver: Экземпляр веб-драйвера
        """
        super().__init__(driver)

    @allure.step("Заполнить форму оформления заказа")
    def fill_form(self, first_name: str, last_name: str, zip_code: str) -> 'CheckoutPage':
        """
        Заполнение формы с персональными данными.

        Args:
            first_name: Имя
            last_name: Фамилия
            zip_code: Почтовый индекс

        Returns:
            Экземпляр страницы оформления заказа для цепочки вызовов
        """
        with allure.step(f"Ввод имени: {first_name}"):
            self.send_keys(*self.FIRST_NAME, first_name)

        with allure.step(f"Ввод фамилии: {last_name}"):
            self.send_keys(*self.LAST_NAME, last_name)

        with allure.step(f"Ввод почтового индекса: {zip_code}"):
            self.send_keys(*self.ZIP_CODE, zip_code)

        with allure.step("Нажатие кнопки 'Continue'"):
            self.click_element(*self.CONTINUE_BUTTON)

        return self

    @allure.step("Получить итоговую сумму заказа")
    def get_total(self) -> str:
        """
        Получение итоговой суммы заказа.

        Returns:
            Текст с итоговой суммой
        """
        total_text = self.get_text(*self.TOTAL_LABEL)
        allure.attach(
            total_text,
            name="Итоговая сумма",
            attachment_type=allure.attachment_type.TEXT
        )
        return total_text