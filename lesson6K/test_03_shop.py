import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def browser():
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_shopping_cart_total(browser):
    browser.get("https://www.saucedemo.com/")
    wait = WebDriverWait(browser, 10)
    
    print(f"Открыта страница: {browser.title}")

    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()
    
    print("Авторизация выполнена")

    items_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt", 
        "Sauce Labs Onesie"
    ]
    
    for item_name in items_to_add:
        try:
            add_button = browser.find_element(
                By.XPATH,
                f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
            )
            add_button.click()
            print(f"Добавлен товар: {item_name}")
        except:
            print(f"Не удалось добавить товар: {item_name}")

    browser.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    print("Перешли в корзину")

    browser.find_element(By.ID, "checkout").click()
    print("Нажали Checkout")

    browser.find_element(By.ID, "first-name").send_keys("Иван")
    browser.find_element(By.ID, "last-name").send_keys("Петров")
    browser.find_element(By.ID, "postal-code").send_keys("123456")
    print("Форма заполнена")
    
    browser.find_element(By.ID, "continue").click()
    print("Нажали Continue")

    total_element = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
    )
    total_text = total_element.text
    print(f"Итоговая сумма: {total_text}")

    total_amount = total_text.replace("Total: $", "")

    assert total_amount == "58.29", f"Ожидалось $58.29, получено ${total_amount}"
    print("Тест пройден успешно!")