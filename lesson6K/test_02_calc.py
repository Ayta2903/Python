import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def test_slow_calculator(browser):
    browser.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
    wait = WebDriverWait(browser, 50)  

    delay_input = browser.find_element(By.CSS_SELECTOR, "#delay")
    delay_input.clear()
    delay_input.send_keys("45")

    browser.find_element(By.XPATH, "//span[text()='7']").click()
    browser.find_element(By.XPATH, "//span[text()='+']").click()
    browser.find_element(By.XPATH, "//span[text()='8']").click()
    browser.find_element(By.XPATH, "//span[text()='=']").click()
    
    print("Выполнено: 7 + 8 =")
    print("Ожидаем 45 секунд...")

    wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".screen"), "15")
    )

    screen = browser.find_element(By.CSS_SELECTOR, ".screen")
    result = screen.text
    print(f"Результат: {result}")
    
    assert result == "15", f"Ожидалось 15, получено {result}"
    print("✓ Тест пройден успешно!")