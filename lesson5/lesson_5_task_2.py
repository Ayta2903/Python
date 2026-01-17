from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10) 

    try:
        driver.get("http://uitestingplayground.com/dynamicid")
        print("Страница загружена")

        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
        )
        button.click()
        print("Синяя кнопка нажата")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()
        print("Браузер закрыт")

if __name__ == "__main__":
    main()
