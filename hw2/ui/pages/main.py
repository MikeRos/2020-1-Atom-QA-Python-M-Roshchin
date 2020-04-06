from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from ui.locators import MainLocators
from .base import BasePage, CannotFindElement


class MainPage(BasePage):

    locators = MainLocators()

    def create_company(self, link, name, picture):
        self.click(self.locators.CAMPAIGN_LIST)
        self.click(self.locators.LINK_CREATE_CAMPAIGN)
        self.click(self.locators.TRAFFIC_TYPE)
        self.completion(link, self.locators.LINK_FIELD)
        self.completion(name, self.locators.NAME_FIELD)
        self.click(self.locators.BANNER)
        download_elem = self.find(self.locators.UPLOAD_ELEMENT)
        download_elem.send_keys(picture)
        self.click(self.locators.SAVE_PIC)
        self.click(self.locators.BUTTON_CREATE_CAMPAIGN)

    def create_segment(self, name):
        self.click(self.locators.BUTTON_SEGMENTS)
        try:
            self.click(self.locators.BUTTON_CREATE_SEGMENT)
        except CannotFindElement:
            self.click(self.locators.LINK_FIRST_SEGMENT)
        self.click(self.locators.ADD_SEGMENTS)
        self.click(self.locators.OPTION_SEGMENT)
        self.click(self.locators.FIRST_CHECKBOX)
        self.click(self.locators.BUTTON_LIST)
        self.click(self.locators.SECOND_CHECKBOX)
        self.click(self.locators.BUTTON_ADD_SEGMENT)
        self.completion(name, self.locators.SEGMENT_NAME_FIELD)
        self.click(self.locators.BUTTON_CONFIRM_SEGMENT)

    def delete_segment(self, name):
        search = self.find(self.locators.SEARCH_SEGMENT)
        search.send_keys(name)
        # Have to wait while searching to get a result
        self.wait().until(EC.visibility_of_element_located(self.locators.SEARCH_SUGGESTION))
        search.send_keys(Keys.RETURN)
        self.click(self.locators.DELETE_BUTTON)
        self.click(self.locators.CONFIRM_DELETE)
