import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import os


@pytest.fixture
def browser():
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    
    driver = webdriver.Edge(options=options)
  
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def test_form_validation(browser):
    browser.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

    print(f"Заголовок страницы: {browser.title}")
    print(f"URL: {browser.current_url}")

    wait = WebDriverWait(browser, 10)

    first_name = wait.until(
        EC.presence_of_element_located((By.ID, "first-name"))
    )
    print("Форма загружена")

    fields = {
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

    for field_id, value in fields.items():
        element = browser.find_element(By.ID, field_id)
        element.clear()
        element.send_keys(value)
        print(f"Заполнено поле {field_id}")

    zip_element = browser.find_element(By.ID, "zip-code")
    zip_element.clear()
    print("Поле zip-code оставлено пустым")

    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("arguments[0].scrollIntoView(true);", submit_button)

    wait.until(EC.element_to_be_clickable(submit_button))

    browser.execute_script("arguments[0].click();", submit_button)
    print("Кнопка Submit нажата")

    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#zip-code.is-invalid"))
        )
    except:
        import time
        time.sleep(2)

    zip_field = browser.find_element(By.ID, "zip-code")
    zip_classes = zip_field.get_attribute("class")
    print(f"Классы zip-code: {zip_classes}")
    
    assert "is-invalid" in zip_classes, f"Zip code должен быть красным. Классы: {zip_classes}"
    print("✓ Zip code подсвечен красным")

    for field_id in fields.keys():
        field = browser.find_element(By.ID, field_id)
        field_classes = field.get_attribute("class")
        
        if "is-valid" not in field_classes:
            print(f"Поле {field_id}: {field_classes}")
        
        assert "is-valid" in field_classes, f"Поле {field_id} должно быть зеленым. Классы: {field_classes}"
    
    print("✓ Все остальные поля подсвечены зеленым")
    print("Тест пройден успешно!")