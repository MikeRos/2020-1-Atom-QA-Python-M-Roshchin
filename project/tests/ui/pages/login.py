from selenium.webdriver.common.keys import Keys

from data.urls import URL_LOGIN
from ui.locators import LoginLocators
from .base import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(URL_LOGIN)

    locators = LoginLocators()

    def login(self, username, password):
        username_field = self.find(self.locators.INPUT_USERNAME)
        password_field = self.find(self.locators.INPUT_PASSWORD)
        username_field.clear()
        password_field.clear()
        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
