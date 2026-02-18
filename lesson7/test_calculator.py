from selenium import webdriver
from lesson7.pages.calculator_page import CalculatorPage


def test_calculator():
    driver = webdriver.Chrome()
    calculator_page = CalculatorPage(driver)
    
    try:
        calculator_page.open()
        calculator_page.set_delay(45)
        
        calculator_page.click_button('7')
        calculator_page.click_button('+')
        calculator_page.click_button('8')
        calculator_page.click_button('=')
        
        result = calculator_page.wait_for_result(50, "15")
        
        assert result == "15", f"Ожидалось 15, получено {result}"
        print(f"Тест пройден! Результат: {result}")
        
    finally:
        driver.quit()


if __name__ == "__main__":
    test_calculator()