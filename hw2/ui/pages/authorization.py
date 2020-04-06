from selenium.webdriver.common.keys import Keys
from ui.locators import AuthLocators
from .base import BasePage


class AuthorizationPage(BasePage):
    locators = AuthLocators()

    def login(self, email, password):
        self.click(self.locators.ENTER_BUTTON)
        email_field = self.find(self.locators.EMAIL)
        password_field = self.find(self.locators.PASSWORD)
        email_field.clear()
        password_field.clear()
        email_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
