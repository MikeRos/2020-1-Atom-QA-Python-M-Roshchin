from selenium.webdriver.common.by import By


class LoginLocators:
    LINK_REG = (By.XPATH, '//a[@href="/reg"]')
    INPUT_USERNAME = (By.XPATH, '//input[@id="username"]')
    INPUT_PASSWORD = (By.XPATH, '//input[@id="password"]')
    BUTTON_SUBMIT = (By.XPATH, '//input[@id="submit"]')
    TEXT_HINT = (By.XPATH, '//div[@id="flash"]')


class RegLocators:
    LINK_LOGIN = (By.XPATH, '//a[@href="/login"]')
    INPUT_USERNAME = (By.XPATH, '//input[@id="username"]')
    INPUT_EMAIL = (By.XPATH, '//input[@id="email"]')
    INPUT_PASSWORD = (By.XPATH, '//input[@id="password"]')
    INPUT_PASSWORD_CONFIRM = (By.XPATH, '//input[@id="confirm"]')
    INPUT_CHECKBOX = (By.XPATH, '//input[@type="checkbox"]')
    BUTTON_SUBMIT = (By.XPATH, '//input[@id="submit"]')
    TEXT_HINT = (By.XPATH, '//div[@id="flash"]')


class MainLocators:
    TEXT_USERNAME = (By.XPATH, '//div[@id="login-name"]//li[1]')
    TEXT_VKID = (By.XPATH, '//div[@id="login-name"]//li[2]')
    LINK_BRAND = (By.XPATH, '//a[@class="uk-navbar-brand uk-hidden-small"]')
    LINK_HOME = (By.XPATH, '//li//a[@href="/"]')
    LINK_LOGOUT = (By.XPATH, '//a[@href="/logout"]')
    LINK_API = (By.XPATH, '//div[@class="uk-grid uk-margin-large-top uk-width-1-2 uk-container-center"]/div[1]//a')
    LINK_INTERNET = (By.XPATH, '//div[@class="uk-grid uk-margin-large-top uk-width-1-2 uk-container-center"]/div[2]//a')
    LINK_SMTP = (By.XPATH, '//div[@class="uk-grid uk-margin-large-top uk-width-1-2 uk-container-center"]/div[3]//a')
    LINK_PYTHON = (By.XPATH, '//*[starts-with(@class, "uk-parent")][1]')
    LINK_HISTORY = (By.XPATH, '//*[starts-with(@class, "uk-parent")][1]//li[1]/a')
    LINK_FLASK = (By.XPATH, '//*[starts-with(@class, "uk-parent")][1]//li[2]/a')
    LINK_LINUX = (By.XPATH, '//li[3]/a')
    LINK_CENTOS = (By.XPATH, '//li[3]//li//a')
    LINK_NETWORK = (By.XPATH, '//li[4]/a')
    LINK_NEWS = (By.XPATH, '//li[4]//li[1]//li[1]//a')
    LINK_DOWNLOAD = (By.XPATH, '//li[4]//li[1]//li[2]//a')
    LINK_EXAMPLES = (By.XPATH, '//li[4]//li[2]//li//a')
    TEXT_MOTIVATION = (By.XPATH, '//footer//p[2]')
