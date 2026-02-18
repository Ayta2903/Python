from selenium import webdriver
from lesson7.pages.avto_page import LoginPage  


class TestSauceDemo:
    def setup_method(self):
        """Создание драйвера"""
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
    
    def teardown_method(self):
        """Закрытие драйвера"""
        self.driver.quit()
    
    def test_total_price(self):
        """Тест проверки итоговой суммы"""
        
        login_page = LoginPage(self.driver)
        inventory_page = login_page.open().login("standard_user", "secret_sauce")

        inventory_page.add_items()

        cart_page = inventory_page.go_to_cart()

        checkout_page = cart_page.checkout()

        checkout_page.fill_form("Aytalina", "Ivanova", "123456")

        total = checkout_page.get_total()
        print(f"\nИтоговая сумма: {total}")

        assert total == "Total: $58.29", f"Ожидалось 'Total: $58.29', получено '{total}'"
        print("Тест пройден успешно!")

