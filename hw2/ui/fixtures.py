import os
import random
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from data.auth import AUTH
from ui.pages.main import MainPage
from ui.pages.authorization import AuthorizationPage


class UndefinedBrowser(Exception):
    pass


@pytest.fixture(scope="function")
def driver(config):
    browser = config['browser']
    version = config['version']
    selenoid = config['selenoid']
    url = config['url']
    if browser == "chrome":
        if not selenoid:
            manager = ChromeDriverManager(version=version)
            driver = webdriver.Chrome(executable_path=manager.install())
        else:
            capabilities = {
                'acceptInsecureCerts': True,
                'browserName': browser,
                'version': '80.0'
            }
            options = ChromeOptions()
            driver = webdriver.Remote(command_executor=selenoid,
                                      options=options,
                                      desired_capabilities=capabilities)
    else:
        raise UndefinedBrowser(f'Wrong browser:{browser} Only "chrome" is now supported')
    driver.maximize_window()
    driver.get(url)
    yield driver
    driver.close()


@pytest.fixture(scope="function")
def get_auth_page(driver):
    return AuthorizationPage(driver)


@pytest.fixture(scope="function")
def get_main_page(driver):
    page = AuthorizationPage(driver)
    page.login(AUTH.get('email'), AUTH.get('password'))
    return MainPage(page.driver)


@pytest.fixture(scope='function')
def test_name():
    return "test_name" + str(random.randint(1, 1000))


@pytest.fixture(scope="function")
def upload_file():
    fixtures_path = os.path.dirname(__file__)
    path = os.path.join(fixtures_path, "..", "data", "pic.png")
    path = os.path.abspath(path)
    return path
