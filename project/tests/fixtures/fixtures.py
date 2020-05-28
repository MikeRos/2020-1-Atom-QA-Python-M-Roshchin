import string

import allure
import pytest
import random
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from api.api_client import APIClient
from data.testing_data import invalid_reg_data, ADMIN_USERNAME, ADMIN_PASSWORD
from db.db_client import DBClient

from exeptions import UndefinedBrowser
from ui.pages.reg import RegPage
from ui.pages.login import LoginPage
from ui.pages.main import MainPage


# Some useful fixtures
# MAGIC! works only with my mock
@pytest.fixture(scope='function')
def get_name_vk_id(string):
    my_little_hash = 0
    for s in string:
        my_little_hash += ord(s)
    if my_little_hash % 10 > 7:
        return None
    # Trying to return something that looks like id
    vk_id = 'vk_' + str(int.from_bytes(string.encode(), 'little') % 10000000)
    return vk_id


@pytest.fixture(scope='function')
def api_client():
    client = APIClient()
    client.login(ADMIN_USERNAME, ADMIN_PASSWORD)
    return client


db_client = DBClient()


@pytest.fixture(scope='function')
def db_session():
    return db_client.get_session()


@pytest.fixture(scope='function')
def get_invalid_user():
    return random.choice(invalid_reg_data)


# Data fixtures


@pytest.fixture(scope='function')
def tst_vk_id():
    return 'vk_'+random.randint(10**7, 10**8)


@pytest.fixture(scope='function')
def tst_password():
    length = random.randint(5, 16)
    password = ''
    for i in range(length):
        password += random.choice(string.ascii_letters)
    return password


@pytest.fixture(scope='function')
def tst_email():
    login_length = random.randint(3, 8)
    login = ''
    address_length = random.randint(3, 8)
    address = ''
    domen_length = random.randint(2, 4)
    domen = ''
    for i in range(login_length):
        login += random.choice(string.ascii_letters)
    for i in range(address_length):
        address += random.choice(string.ascii_letters)
    for i in range(domen_length):
        domen += random.choice(string.ascii_letters)
    return login+'@'+address+'.'+domen


@pytest.fixture(scope='function')
def tst_username():
    length = random.randint(7, 12)
    username = ''
    for i in range(length):
        username += random.choice(string.ascii_letters)
    return username


# UI fixtures

@pytest.fixture(scope="function")
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture(scope="function")
def reg_page(driver):
    return RegPage(driver)


@pytest.fixture(scope="function")
def main_page(driver):
    return MainPage(driver)


@pytest.fixture(scope="function")
def logged_main_page(driver):
    page = LoginPage(driver)
    page.login(ADMIN_USERNAME, ADMIN_PASSWORD)
    return MainPage(page.driver)


@pytest.fixture(scope="function")
def driver(config, request):
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
                'version': '80.0',
                'enableVNC': True
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
    if request.node.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(), name=request.function.__name__, attachment_type=allure.attachment_type.PNG)
    driver.quit()
