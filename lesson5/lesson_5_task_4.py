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
    wait = WebDriverWait(driver, 20)  

    try:
        driver.get("http://the-internet.herokuapp.com/login")
        print("Страница авторизации загружена")

        username_field = wait.until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        username_field.send_keys("tomsmith")
        print('Введён логин "tomsmith"')

        password_field = wait.until(
            EC.element_to_be_clickable((By.ID, "password"))
        )
        password_field.send_keys("SuperSecretPassword!")
        print('Введён пароль "SuperSecretPassword!"')

        login_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        print("Кнопка Login нажата")

        driver.save_screenshot("after_login.png")

        success_message = wait.until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        message_text = success_message.text.strip()
        print(f"Текст с зелёной плашки: {message_text}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        driver.save_screenshot("error_screenshot.png")
        raise
    finally:
        driver.quit()
        print("Браузер закрыт")

if __name__ == "__main__":
     main()