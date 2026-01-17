from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_ajax_button():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("http://uitestingplayground.com/ajax")
        print("Страница загружена")

        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#ajaxButton"))
        )
        button.click()
        print("Кнопка нажата")


        success_message = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".bg-success"))
        )
        message_text = success_message.text.strip()

        # Вывод текста в консоль
        print(f"Текст из зелёной плашки: {message_text}")

        # Проверка ожидаемого текста
        assert message_text == "Data loaded with AJAX get request.", \
            f"Ожидался текст 'Data loaded with AJAX get request.', но получен: '{message_text}'"

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise
    finally:
        driver.quit()
        print("Браузер закрыт")

if __name__ == "__main__":
    test_ajax_button()
