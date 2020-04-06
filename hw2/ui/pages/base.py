from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


RETRY_COUNT = 3


class CannotFindElement(Exception):
    pass


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def find(self, locator, timeout=None) -> WebElement:
        try:
            result = self.wait(timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise CannotFindElement
        return result

    def click(self, locator, timeout=None):
        for i in range(RETRY_COUNT):
            try:
                self.find(locator)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()

            # Element is found but we cannot click it
            except TimeoutException:
                raise CannotFindElement

            # Element actually not found
            except CannotFindElement:
                raise CannotFindElement

            except StaleElementReferenceException:
                if i < RETRY_COUNT - 1:
                    pass
            return

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def completion(self, text, locator):
        for i in range(RETRY_COUNT):
            try:
                link_field = self.find(locator)
                self.click(locator)
                link_field.clear()
                link_field.send_keys(text)
                break

            except StaleElementReferenceException:
                if i < RETRY_COUNT - 1:
                    pass
