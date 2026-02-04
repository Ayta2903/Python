from selenium import webdriver
from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
    
    def open(self):
        self.driver.get("https://www.saucedemo.com/")
        return self
    
    def login(self, username, password):
        self.driver.find_element(By.ID, "user-name").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()
        return InventoryPage(self.driver)


class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
    
    def add_items(self):
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt").click()
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie").click()
        return self
    
    def go_to_cart(self):
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        return CartPage(self.driver)


class CartPage:
    def __init__(self, driver):
        self.driver = driver
    
    def checkout(self):
        self.driver.find_element(By.ID, "checkout").click()
        return CheckoutPage(self.driver)


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
    
    def fill_form(self, first, last, zip_code):
        self.driver.find_element(By.ID, "first-name").send_keys(first)
        self.driver.find_element(By.ID, "last-name").send_keys(last)
        self.driver.find_element(By.ID, "postal-code").send_keys(zip_code)
        self.driver.find_element(By.ID, "continue").click()
        return self
    
    def get_total(self):
        return self.driver.find_element(By.CLASS_NAME, "summary_total_label").text



def main():
    driver = webdriver.Firefox()
    
    try:
        login = LoginPage(driver)
        inventory = login.open().login("standard_user", "secret_sauce")
        
        inventory.add_items()
        
        cart = inventory.go_to_cart()
        checkout = cart.checkout()
        
        checkout.fill_form("Aytalina", "Ivanova", "Yakutsk")

        total = checkout.get_total()
        print(f"Итоговая сумма: {total}")
        
        assert total == "Total: $58.29", f"Ожидалось 'Total: $58.29', получено '{total}'"
        
        print("\n" + "="*50)
        print("ТЕСТ ПРОЙДЕН УСПЕШНО!")
        print(f"Итоговая сумма верна: {total}")
        print("="*50)
        
    except Exception as e:
        print(f"\nОШИБКА: {e}")
        driver.save_screenshot("error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()