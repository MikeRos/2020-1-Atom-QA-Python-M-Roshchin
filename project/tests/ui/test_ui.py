from time import sleep

import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.exc import IntegrityError

from base_ui import BaseCase
from data.urls import URL_MAIN, URL_LOGIN, URL_REG, URL_DEFAULT
from data.testing_data import ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_VK_ID, invalid_reg_parametrization
from exeptions import UnexpectedDBData, DBDataNotFound, NoNewTab
from locators import MainLocators, LoginLocators, RegLocators
from db.model import User


@pytest.mark.UI
@pytest.mark.Positive
@pytest.mark.LoginPage
class TestLoginPositive(BaseCase):
    def test_login_page(self, login_page):
        """Testing:
        that login page is displayed

        Steps:
        - open app default url

        Expected result:
        - login page is displayed
        """
        self.page = login_page
        assert self.page.find(LoginLocators.INPUT_USERNAME)

    def test_login_allowed_user(self, login_page, db_session, tst_username, tst_email, tst_password):
        """Testing:
        that user with valid <username>, <password> is logged after submitting form

        Steps:
        - add test user to DB
        - fill login form with correct data
        - submit login
        (Done via fixtures so test may look confusing)
        - delete test data from DB

        Expected result:
        - Page with .../welcome/ url is opened
        - <username> access and active status in DB is 1
        - "Logged as <username>" message is displayed TODO may be wrong if main page work wrong even if login page is OK
        TODO check start_active_time updating in DB
        """
        try:
            db_session.add(
                User(username=tst_username, password=tst_password, email=tst_email, access=1, active=0))
            db_session.commit()
        except IntegrityError:
            raise UnexpectedDBData()
        self.page = login_page
        self.page.login(tst_username, tst_password)
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert test_user.access == 1 and test_user.active == 1 and self.driver.current_url == URL_MAIN \
               and tst_username in self.page.find(MainLocators.TEXT_USERNAME).text

    def test_login_redirect(self, login_page):
        """Testing:
        that login page redirects to main if user is already authenticated

        Steps:
        - fill login form with correct data
        - submit login
        (Done via fixtures so test may look confusing)
        - get login page

        Expected result:
        - login page redirects to main
        """
        self.page = login_page
        self.page.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        self.driver.get(URL_LOGIN)
        assert self.driver.current_url == URL_MAIN

    def test_reg_link(self, login_page):
        """Testing:
        that login page reg link redirects to reg page

        Steps:
        - click on register link

        Expected result:
        - login page redirects register page
        """
        self.page = login_page
        self.page.click(self.page.locators.LINK_REG)
        assert self.driver.current_url == URL_REG


@pytest.mark.UI
@pytest.mark.Positive
@pytest.mark.RegPage
class TestRegPositive(BaseCase):
    def test_reg_page(self, reg_page):
        """Testing:
        that registration page is displayed

        Steps:
        - open app registration url (/reg)

        Expected result:
        - registration page is displayed
        """
        self.page = reg_page
        assert self.page.find(RegLocators.INPUT_CHECKBOX)

    def test_login_link(self, reg_page):
        """Testing:
        that login page reg link redirects to reg page

        Steps:
        - click on register link

        Expected result:
        - registration page redirects to login page
        """
        self.page = reg_page
        self.page.click(self.page.locators.LINK_LOGIN)
        assert self.driver.current_url == URL_LOGIN

    def test_reg_redirect(self, login_page):
        """Testing:
        that registration page redirects to main if user is already authenticated

        Steps:
        - fill login form with correct data
        - submit login
        (Done via fixtures so test may look confusing)
        - get registration page

        Expected result:
        - registration page redirects to main
        """
        self.page = login_page
        self.page.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        self.driver.get(URL_REG)
        assert self.driver.current_url == URL_MAIN

    def test_valid_reg(self, db_session, reg_page, tst_username, tst_email, tst_password):
        """Testing:
        that user with <username>, <password>, <email> is registered after submitting form
        Test is parametrized to check data validation

        Steps:
        - fill reg form with valid data
        - delete test data from DB

        Expected result:
        - User is registered
        - Page with .../welcome/ url is opened
        - <username> access and active status in DB is 1
        - "Logged as <username>" message is displayed TODO may be wrong if main page work wrong even if login page is OK
        """
        self.page = reg_page
        self.page.register(tst_username, tst_email, tst_password)
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert test_user.access == 1 and test_user.active == 1 and self.driver.current_url == URL_MAIN \
               and tst_username in self.page.find(MainLocators.TEXT_USERNAME).text


@pytest.mark.UI
@pytest.mark.Positive
@pytest.mark.MainPage
class TestMainPositive(BaseCase):
    def test_main_login_as(self, logged_main_page):
        """Testing:
        that main page displays "Logged as <username>"

        Steps:
        - get logged main page

        Expected result:
        - main page displays "Logged as <username>"
        """
        self.page = logged_main_page
        assert self.driver.current_url == URL_MAIN and ADMIN_USERNAME in self.page.find(MainLocators.TEXT_USERNAME).text

    def test_main_vk_id(self, logged_main_page):
        """Testing:
        that main page displays "VK ID: <username>"

        Steps:
        - get logged main page

        Expected result:
        - main page displays "VK ID: vk_id for <username>"
        """
        self.page = logged_main_page
        assert self.driver.current_url == URL_MAIN and ADMIN_VK_ID in self.page.find(MainLocators.TEXT_VKID).text

    def test_main_without_vk_id(self, login_page, db_session, tst_username, tst_email, tst_password):
        """Testing:
        that main page displays "LOGGED as: <username>" and no vk_id because it's unavailable

        Steps:
        - get logged main page

        Expected result:
        - main page displays "LOGGED as: <username>" and no vk_id
        """
        try:
            db_session.add(
                User(username=tst_username, password=tst_password, email=tst_email, access=1, active=0))
            db_session.commit()
        except IntegrityError:
            raise UnexpectedDBData()
        self.page = login_page
        self.page.login(tst_username, tst_password)
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert self.driver.current_url == URL_MAIN and self.page.find(MainLocators.TEXT_VKID)

    def test_home_link(self, logged_main_page):
        """Testing:
        that main page home link routes to main page

        Steps:
        - get logged main page
        - click home link

        Expected result:
        - main page routes to main page
        """
        self.page = logged_main_page
        self.page.find(MainLocators.LINK_HOME).click()
        assert self.driver.current_url == URL_MAIN

    def test_brand_link(self, logged_main_page):
        """Testing:
        that main page brand link routes to main page

        Steps:
        - get logged main page
        - click brand link

        Expected result:
        - main page routes to main page
        """
        self.page = logged_main_page
        self.page.find(MainLocators.LINK_BRAND).click()
        assert self.driver.current_url == URL_MAIN

    def test_python_link(self, logged_main_page):
        """Testing:
        that main page python link routes to correct page

        Steps:
        - get logged main page
        - click python link

        Expected result:
        - link routes to python page
        """
        self.page = logged_main_page
        mouse = ActionChains(self.driver)
        mouse.move_to_element(self.page.find(MainLocators.LINK_PYTHON)).click().perform()
        try:
            self.driver.switch_to_window(self.driver.window_handles[1])
        except IndexError:
            raise NoNewTab()
        assert self.driver.current_url == 'https://www.python.org/'

    def test_python_history_link(self, logged_main_page):
        """Testing:
        that main page python history link routes to correct page

        Steps:
        - get logged main page
        - hover python link
        - click python history link

        Expected result:
        - link routes to python history page
        """
        self.page = logged_main_page
        mouse = ActionChains(self.driver)
        mouse.move_to_element(self.page.find(MainLocators.LINK_PYTHON)).perform()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(MainLocators.LINK_HISTORY))
        mouse.move_to_element(self.page.find(MainLocators.LINK_HISTORY)).click().perform()
        try:
            self.driver.switch_to_window(self.driver.window_handles[1])
        except IndexError:
            raise NoNewTab()
        assert self.driver.current_url == 'https://en.wikipedia.org/wiki/History_of_Python'

    def test_flask_link(self, logged_main_page):
        """Testing:
        that main page flask link routes to correct page

        Steps:
        - get logged main page
        - hover python link
        - click flask link

        Expected result:
        - link routes to flask page
        """
        self.page = logged_main_page
        mouse = ActionChains(self.driver)
        mouse.move_to_element(self.page.find(MainLocators.LINK_PYTHON)).perform()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(MainLocators.LINK_FLASK))
        mouse.move_to_element(self.page.find(MainLocators.LINK_FLASK)).click().perform()
        try:
            self.driver.switch_to_window(self.driver.window_handles[1])
        except IndexError:
            raise NoNewTab()
        assert self.driver.current_url == 'https://flask.palletsprojects.com/en/1.1.x/#'

    def test_centos_link(self, logged_main_page):
        """Testing:
        that main page centos link routes to correct page

        Steps:
        - get logged main page
        - hover linux link
        - click centos link

        Expected result:
        - link routes to centos download page
        """
        self.page = logged_main_page
        mouse = ActionChains(self.driver)
        mouse.move_to_element(self.page.find(MainLocators.LINK_LINUX)).perform()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(MainLocators.LINK_CENTOS))
        mouse.move_to_element(self.page.find(MainLocators.LINK_CENTOS)).click().perform()
        try:
            self.driver.switch_to_window(self.driver.window_handles[1])
        except IndexError:
            raise NoNewTab()
        assert self.driver.current_url == 'https://www.centos.org/download/'

    def test_wireshark_news_link(self, logged_main_page):
        """Testing:
        that main page wireshark news link routes to correct page

        Steps:
        - get logged main page
        - hover network link
        - click wireshark news link

        Expected result:
        - link routes to wireshark news page
        """
        self.page = logged_main_page
        mouse = ActionChains(self.driver)
        mouse.move_to_element(self.page.find(MainLocators.LINK_NETWORK)).perform()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(MainLocators.LINK_NEWS))
        mouse.move_to_element(self.page.find(MainLocators.LINK_NEWS)).click().perform()
        self.driver.switch_to_window(self.driver.window_handles[1])
        assert self.driver.current_url == 'https://www.wireshark.org/news/'

    def test_wireshark_download_link(self, logged_main_page):
        """Testing:
        that main page wireshark download link routes to correct page

        Steps:
        - get logged main page
        - hover network link
        - click wireshark download link

        Expected result:
        - link routes to wireshark download page
        """
        self.page = logged_main_page
        mouse = ActionChains(self.driver)
        mouse.move_to_element(self.page.find(MainLocators.LINK_NETWORK)).perform()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(MainLocators.LINK_DOWNLOAD))
        mouse.move_to_element(self.page.find(MainLocators.LINK_DOWNLOAD)).click().perform()
        self.driver.switch_to_window(self.driver.window_handles[1])
        assert self.driver.current_url == 'https://www.wireshark.org/#download'

    def test_api_link(self, logged_main_page):
        """Testing:
        that main page api link routes to correct page

        Steps:
        - get logged main page
        - hover linux link
        - click centos link

        Expected result:
        - link routes to api wiki page
        """
        self.page = logged_main_page
        mouse = ActionChains(self.driver)
        mouse.move_to_element(self.page.find(MainLocators.LINK_API)).click().perform()
        try:
            self.driver.switch_to_window(self.driver.window_handles[1])
        except IndexError:
            raise NoNewTab()
        assert self.driver.current_url == 'https://en.wikipedia.org/wiki/Application_programming_interface'

    def test_FOI_link(self, logged_main_page):
        """Testing:
        that main page FOI link routes to correct page

        Steps:
        - get logged main page
        - click FOI link

        Expected result:
        - link routes to FOI page
        """
        self.page = logged_main_page
        mouse = ActionChains(self.driver)
        mouse.move_to_element(self.page.find(MainLocators.LINK_INTERNET)).click().perform()
        try:
            self.driver.switch_to_window(self.driver.window_handles[1])
        except IndexError:
            raise NoNewTab()
        assert self.driver.current_url == 'https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/'

    def test_smtp_link(self, logged_main_page):
        """Testing:
        that main page smtp link routes to correct page

        Steps:
        - get logged main page
        - click smtp link

        Expected result:
        - link routes to smtp wiki page
        """
        self.page = logged_main_page
        mouse = ActionChains(self.driver)
        mouse.move_to_element(self.page.find(MainLocators.LINK_SMTP)).click().perform()
        try:
            self.driver.switch_to_window(self.driver.window_handles[1])
        except IndexError:
            raise NoNewTab()
        assert self.driver.current_url == 'https://en.wikipedia.org/wiki/SMTP'

    def test_motivation(self, db_session, login_page, tst_username, tst_email, tst_password):
        """Testing:
        that main page motivation message id displayed

        Steps:
        - get logged main page

        Expected result:
        - main page footer motivation message id displayed
        """
        try:
            db_session.add(
                User(username=tst_username, password=tst_password, email=tst_email, access=1, active=0))
            db_session.commit()
        except IntegrityError:
            raise UnexpectedDBData()
        self.page = login_page
        self.page.login(tst_username, tst_password)
        motivation = self.page.find(MainLocators.TEXT_MOTIVATION)
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert motivation is not None

    def test_logout(self, db_session, logged_main_page):
        """Testing:
        that main page logout link routes to login page and user is logged out

        Steps:
        - get logged main page
        - click logout link

        Expected result:
        - main page routes to login page
        - <username> access and active status in DB is 0
        """
        self.page = logged_main_page
        self.page.find(MainLocators.LINK_LOGOUT).click()
        test_user = db_session.query(User).filter_by(username=ADMIN_USERNAME).first()
        db_session.commit()
        assert self.driver.current_url == URL_LOGIN and test_user.active == 0


@pytest.mark.UI
@pytest.mark.Negative
@pytest.mark.LoginPage
class TestLoginNegative(BaseCase):
    def test_login_disallowed_user(self, login_page, db_session, tst_username, tst_email, tst_password):
        """Testing:
        that user with access status 0 and <username>, <password> is not authorized after submitting form

        Steps:
        - add test user to DB
        - fill login form with test data
        - submit login
        (Done via fixtures so test may look confusing)

        Expected result:
        - Block hint is displayed
        - <username> access and active status in DB is 0
        """
        hint_msg = 'Ваша учетная запись заблокирована'
        try:
            db_session.add(
                User(username=tst_username, password=tst_password, email=tst_email, access=0, active=0))
            db_session.commit()
        except IntegrityError:
            raise UnexpectedDBData()
        self.page = login_page
        self.page.login(tst_username, tst_password)
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert test_user.access == 0 and test_user.active == 0 and self.driver.current_url == URL_LOGIN\
               and hint_msg in self.page.find(LoginLocators.TEXT_HINT).text

    def test_login_disallowed_active_user(self, login_page, db_session, tst_username, tst_email, tst_password):
        """Testing:
        that user with access status 0 but active 1 and <username>, <password> is not authorized after submitting form

        Steps:
        - add test user to DB
        - fill login form with test data
        - submit login
        (Done via fixtures so test may look confusing)

        Expected result:
        - Block hint is displayed
        - <username> access and active status in DB is 0
        """
        hint_msg = 'Ваша учетная запись заблокирована'
        try:
            db_session.add(
                User(username=tst_username, password=tst_password, email=tst_email, access=0, active=1))
            db_session.commit()
        except IntegrityError:
            raise UnexpectedDBData()
        self.page = login_page
        self.page.login(tst_username, tst_password)
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert test_user.access == 0 and test_user.active == 1 and self.driver.current_url == URL_LOGIN\
               and hint_msg in self.page.find(LoginLocators.TEXT_HINT).text

    def test_login_non_existing_user(self, login_page, db_session, tst_username, tst_email, tst_password):
        """Testing:
        that user with non existing <username>, <password> is not authorized

        Steps:
        - fill login form with test data
        - submit login

        Expected result:
        - Block hint is displayed
        - <username> access and active status in DB is 0
        """
        hint_msg = 'Invalid username or password'
        self.page = login_page
        self.page.login(tst_username, tst_password)
        sleep(0.5)  # BLACK MAGIC!!! Have to wait to get filled hint message instead of empty - ''
        assert self.driver.current_url == URL_LOGIN and hint_msg in self.page.find(LoginLocators.TEXT_HINT).text

    def test_login_short_name(self, login_page, db_session, tst_username, tst_email, tst_password):
        """Testing:
        that authorization with too short name

        Steps:
        - fill login form with test data
        - submit login

        Expected result:
        - Hint is displayed
        """
        hint_msg = 'Incorrect username length'
        self.page = login_page
        self.page.login(tst_username[0], tst_password)
        sleep(0.5)  # BLACK MAGIC!!! Have to wait to get filled hint message instead of empty - ''
        assert self.driver.current_url == URL_LOGIN and hint_msg in self.page.find(LoginLocators.TEXT_HINT).text

    def test_login_long_name(self, login_page, db_session, tst_username, tst_password, tst_email):
        """Testing:
        that authorization with too long name

        Steps:
        - fill login form with test data
        - submit login

        Expected result:
        - Hint is displayed
        """
        hint_msg = 'Incorrect username length'
        self.page = login_page
        self.page.login(tst_username[0]*100, tst_password)
        sleep(0.5)  # BLACK MAGIC!!! Have to wait to get filled hint message instead of empty - ''
        assert self.driver.current_url == URL_LOGIN and hint_msg in self.page.find(LoginLocators.TEXT_HINT).text


@pytest.mark.UI
@pytest.mark.Negative
@pytest.mark.RegPage
class TestRegNegative(BaseCase):
    # TODO not sure if pass validation is described in requirements
    # TODO not sure if proper hint message is described in requirements

    def test_existing_name_reg(self, db_session, reg_page, tst_username, tst_email, tst_password):
        """Testing:
        that user with <username>, <password>, <email> is registered after submitting form

        Steps:
        - fill reg form with valid data
        - submit registration
        - fill reg form with same data but different email

        Expected result:
        - User is not registered
        - hint message is displayed
        """
        hint_msg = "User already exist"
        self.page = reg_page
        self.page.register(tst_username, tst_email, tst_password)
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        if test_user is None:
            raise DBDataNotFound
        self.page.find(MainLocators.LINK_LOGOUT).click()
        # sleep(0.5)
        self.driver.get(URL_REG)
        self.page.register(tst_username, tst_email[1:], tst_password)
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert self.driver.current_url == URL_REG \
               and hint_msg in self.page.find(RegLocators.TEXT_HINT).text

    def test_existing_mail_reg(self, db_session, reg_page, tst_username, tst_email, tst_password):
        """Testing:
        that user with <username>, <password>, <email> is registered after submitting form

        Steps:
        - fill reg form with valid data
        - submit registration
        - fill reg form with same data but different username

        Expected result:
        - User is not registered
        - hint message is displayed
        """
        hint_msg = "User already exist"  # TODO not sure if message should be like this
        self.page = reg_page
        self.page.register(tst_username, tst_email, tst_password)
        sleep(1)  # BLACK MAGIC!!! Have to wait
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        if test_user is None:
            raise DBDataNotFound
        self.page.find(MainLocators.LINK_LOGOUT).click()
        self.driver.get(URL_REG)
        self.page.register(tst_username[1:], tst_email, tst_password)
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert self.driver.current_url == URL_REG \
               and hint_msg in self.page.find(RegLocators.TEXT_HINT).text

    @pytest.mark.parametrize("invalid_reg_data", invalid_reg_parametrization)
    def test_invalid_reg(self, db_session, reg_page, invalid_reg_data):
        """Testing:
        that registration of user with <username>, <email>, <password>, <password_confirmation> is denied and proper hint is displayed

        Steps:
        - fill reg form with invalid data (see test parameter)
        - submit registration

        Expected result:
        - User is not registered
        - proper hint message is displayed
        """
        user = invalid_reg_data[:-1]
        hint_msg = invalid_reg_data[4]
        self.page = reg_page
        self.page.register(user[0], user[1], user[2], user[3])
        test_user = db_session.query(User).filter_by(username=user[0]).first()
        db_session.commit()
        sleep(0.5)  # BLACK MAGIC!!! Have to wait to get filled hint message instead of empty - ''
        assert test_user is None and self.driver.current_url == URL_REG \
               and hint_msg in self.page.find(RegLocators.TEXT_HINT).text


@pytest.mark.UI
@pytest.mark.Negative
@pytest.mark.MainPage
class TestMainNegative(BaseCase):
    def test_main_redirect(self, main_page):
        """Testing:
        that main page redirects to default url if user is not authenticated

        Steps:
        - get main page

        Expected result:
        - main page redirects to default page
        """
        self.page = main_page
        assert self.driver.current_url == URL_DEFAULT
