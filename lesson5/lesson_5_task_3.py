from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    firefox_options = Options()
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Firefox(options=firefox_options)
    wait = WebDriverWait(driver, 10)  

    try:
        driver.get("http://the-internet.herokuapp.com/inputs")
        print("Страница загружена")

        input_field = wait.until(
            EC.element_to_be_clickable((By.TAG_NAME, "input"))
        )
        print("Поле ввода найдено")

        input_field.send_keys("Sky")
        print('Введён текст "Sky"')

        input_field.clear()
        print("Поле очищено")

        input_field.send_keys("Pro")
        print('Введён текст "Pro"')

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()
        print("Браузер закрыт")

if __name__ == "__main__":
    main()
