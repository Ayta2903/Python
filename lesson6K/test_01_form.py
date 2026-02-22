import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

@pytest.fixture
def driver():
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_form_submission_simple(driver):
    """Упрощённая версия с проверкой CSS-классов"""

    # Исправление URL: https:// → https://
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")
    print("\n=== Начало теста (упрощённая версия) ===")

    # Заполняем поля
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
            field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, field_name))
            )
            field.clear()
            field.send_keys(value)
            print(f"✓ Поле '{field_name}' заполнено")
        except TimeoutException:
            pytest.fail(f"Поле {field_name} не найдено на странице в течение 10 секунд")

    # Zip code оставляем пустым
    try:
        zip_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "zip-code"))
        )
        zip_field.clear()
        print("⚠ Поле 'zip-code' пустое")
    except TimeoutException:
        pytest.fail("Поле 'zip-code' не найдено на странице")

    # Отправляем форму
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()
        print("✓ Кнопка Submit нажата")
    except TimeoutException:
        try:
            submit_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            submit_button.click()
            print("✓ Кнопка Submit нажата (альтернативный селектор)")
        except TimeoutException:
            pytest.fail("Кнопка Submit не найдена на странице")

    # Явное ожидание появления сообщений валидации
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "zip-code"))
    )

    print("\n=== Проверка классов валидации ===")

    # Проверяем поле Zip code (должно быть подсвечено красным)
    try:
        zip_code_field = driver.find_element(By.ID, "zip-code")
        zip_classes = zip_code_field.get_attribute("class")
        print(f"Zip code классы: {zip_classes}")

        # Проверка на наличие класса ошибки (обычно is-invalid или alert-danger)
        assert "is-invalid" in zip_classes or "alert-danger" in zip_classes, \
            "Поле Zip code не подсвечено красным (класс is-invalid/alert-danger отсутствует)"
        print("✓ Поле Zip code подсвечено красным (есть класс is-invalid/alert-danger)")
    except NoSuchElementException:
        pytest.fail("Поле Zip code (name='zip-code') не найдено на странице")

    # Проверяем остальные поля (должны быть подсвечены зелёным)
    for field_name in fields_to_fill.keys():
        try:
            field = driver.find_element(By.ID, field_name)
            field_classes = field.get_attribute("class")
            assert "is-valid" in field_classes or "alert-success" in field_classes, \
                f"Поле {field_name} не подсвечено зелёным (класс is-valid/alert-success отсутствует)"
            print(f"✓ Поле {field_name} подсвечено зелёным (есть класс is-valid/alert-success)")
        except NoSuchElementException:
            pytest.fail(f"Поле {field_name} не найдено на странице")

    print("\n" + "=" * 50)
    print("ТЕСТ ПРОЙДЕН УСПЕШНО!")
    print("=" * 50)
