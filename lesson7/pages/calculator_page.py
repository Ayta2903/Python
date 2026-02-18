from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
        
    def open(self):
        self.driver.get(self.url)
        return self
    
    def set_delay(self, delay_value):
        delay_field = self.driver.find_element(By.CSS_SELECTOR, "#delay")
        delay_field.clear()
        delay_field.send_keys(str(delay_value))
        return self
    
    def click_button(self, button):
        button_map = {
            '7': "//span[text()='7']",
            '8': "//span[text()='8']",
            '+': "//span[text()='+']",
            '=': "//span[text()='=']",
        }
        if button in button_map:
            button_element = self.driver.find_element(By.XPATH, button_map[button])
            button_element.click()
        return self
    
    def get_display_text(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".screen").text
    
    def wait_for_result(self, timeout, expected_result):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".screen"), str(expected_result))
        )
        return self.get_display_text()