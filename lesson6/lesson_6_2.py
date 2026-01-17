from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_rename_button():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("http://uitestingplayground.com/textinput")
        print("Страница загружена")

        input_field = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#newButtonName"))
        )
        input_field.send_keys("SkyPro")
        print('Введён текст "SkyPro"')

        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#updatingButton"))
        )
        button.click()
        print("Кнопка нажата")

        wait.until(
            lambda driver: button.text != "Set New Button Name"
        )

        updated_button_text = button.text
        print(f"Текст кнопки после обновления: {updated_button_text}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise
    finally:
        driver.quit()
        print("Браузер закрыт")

if __name__ == "__main__":
    test_rename_button()
