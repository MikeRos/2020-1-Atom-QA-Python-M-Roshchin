import pytest
from ui.pages.base import BasePage


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        self.page = BasePage(self.driver)
