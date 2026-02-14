import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


@pytest.fixture
def driver():
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_form_submission(driver):
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

    fields_to_fill = {
        "first-name": "Иван",
        "last-name": "Петров",
        "address": "Ленина, 55-3",
        "e-mail": "test@skypro.com",
        "phone": "+7985899998787",
        "city": "Москва",
        "country": "Россия",
        "job-position": "QA",
        "company": "SkyPro"
    }

    for field_name, value in fields_to_fill.items():
        try:
            field = driver.find_element(By.NAME, field_name)
            field.send_keys(value)
        except NoSuchElementException:
            pytest.fail(f"Поле с name='{field_name}' не найдено на странице")


    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-outline-primary"))
        )
        submit_button.click()
    except TimeoutException:
        pytest.fail("Кнопка Submit не стала кликабельной за 10 секунд")


    try:
        zip_code_field = driver.find_element(By.NAME, "zip-code")
        assert "is-invalid" in zip_code_field.get_attribute("class"), \
            "Поле Zip code не подсвечено красным (класс is-invalid)"
    except NoSuchElementException:
        pytest.fail("Поле Zip code (name='zip-code') не найдено на странице")


    for field_name in fields_to_fill.keys():
        try:
            field = driver.find_element(By.NAME, field_name)
            assert "is-valid" in field.get_attribute("class"), \
                f"Поле {field_name} не подсвечено зелёным (класс is-valid)"
        except NoSuchElementException:
            pytest.fail(f"Поле {field_name} не найдено на странице")
