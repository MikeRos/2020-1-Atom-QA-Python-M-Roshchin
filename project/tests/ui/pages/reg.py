from selenium.webdriver.common.keys import Keys
from ui.locators import RegLocators
from .base import BasePage
from data.urls import URL_REG


class RegPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(URL_REG)

    locators = RegLocators()

    def register(self, username, email, password, password_c=None):
        if password_c is None:
            password_c = password
        username_field = self.find(self.locators.INPUT_USERNAME)
        email_field = self.find(self.locators.INPUT_EMAIL)
        password_field = self.find(self.locators.INPUT_PASSWORD)
        password_confirm_field = self.find(self.locators.INPUT_PASSWORD_CONFIRM)
        checkbox = self.find(self.locators.INPUT_CHECKBOX)
        username_field.clear()
        email_field.clear()
        password_field.clear()
        password_confirm_field.clear()
        username_field.send_keys(username)
        email_field.send_keys(email)
        password_field.send_keys(password)
        password_confirm_field.send_keys(password_c)
        checkbox.click()
        password_field.send_keys(Keys.RETURN)
