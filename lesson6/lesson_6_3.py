from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_wait_for_images():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 30)  

    try:

        driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")
        print("Страница загружена")

        image_container = wait.until(
            EC.visibility_of_element_located((By.ID, "image-container"))
        )
        print("Контейнер с изображениями виден")

        wait.until(
            lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "#image-container img")) >= 3
        )
        print("Достаточно изображений загружено")

        images = driver.find_elements(By.CSS_SELECTOR, "#image-container img")

        if len(images) < 3:
            error_msg = f"В контейнере найдено только {len(images)} изображений. Ожидали минимум 3."
            print(error_msg)
            raise IndexError(error_msg)

        third_image_src = images[2].get_attribute("src")

        print(f"Значение атрибута src 3‑й картинки: {third_image_src}")

        assert third_image_src, "Атрибут src 3‑й картинки пуст"

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise
    finally:
        driver.quit()
        print("Браузер закрыт")

if __name__ == "__main__":
    test_wait_for_images()
