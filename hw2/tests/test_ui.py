import pytest
from selenium.webdriver.common.keys import Keys
from tests.base_ui import BaseCase
from api.urls import URLS


@pytest.mark.UI
class TestUi(BaseCase):
    def test_auth(self, get_main_page):
        self.page = get_main_page
        assert self.page.find(self.page.locators.USER_NAME) is not None

    def test_auth_fail(self, get_auth_page):
        self.page = get_auth_page
        self.page.login('test@testmail.tst', 'password42')
        assert URLS.get('error_url') in self.driver.current_url

    def test_create_campaign(self, get_main_page, test_name, upload_file):
        self.page = get_main_page
        self.page.create_campaign('target.my.com', test_name, upload_file)
        element = self.page.find(self.page.locators.CAMPAIGN_NAME)
        assert element.get_attribute("text") == test_name

    def test_create_segment(self, get_main_page, test_name):
        self.page = get_main_page
        self.page.create_segment(test_name)
        # Have to sort to get last segment if there are any other
        self.page.click(self.page.locators.BUTTON_SORT)
        self.page.click(self.page.locators.BUTTON_SORT)
        element = self.page.find(self.page.locators.SEGMENT_NAME)
        assert element.get_attribute("text") == test_name

    def test_delete_segment(self, get_main_page, test_name):
        result = False
        self.page = get_main_page
        self.page.create_segment(test_name)
        while self.driver.current_url != "https://target.my.com/segments/segments_list":
            pass
        self.page.delete_segment(test_name)
        self.driver.refresh()
        print(self.page.find(self.page.locators.SEGMENT_COUNTER).text)
        if self.page.find(self.page.locators.SEGMENT_COUNTER).text == '0':
            result = True
        else:
            self.page.completion(test_name, self.page.locators.SEARCH_SEGMENT)
            self.page.find(self.page.locators.SEARCH_SEGMENT).send_keys(Keys.RETURN)
            element = self.page.find(self.page.locators.EMPTY_SUGGESTION)
            if element:
                result = True
        assert result
