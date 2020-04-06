from selenium.webdriver.common.by import By


class AuthLocators:
    ENTER_BUTTON = (By.CLASS_NAME, 'responseHead-module-button-1BMAy4')
    EMAIL = (By.NAME, 'email')
    PASSWORD = (By.NAME, 'password')


class MainLocators:

    USER_NAME = (By.CLASS_NAME, 'right-module-userNameWrap-34ibLS')
    CAMPAIGN_NAME = (By.XPATH, '//div[@class="campaign-title-top"]/a')
    CAMPAIGN_LIST = (By.XPATH, '//a[@href="/campaigns/full"]')
    LINK_CREATE_CAMPAIGN = (By.CLASS_NAME, 'campaigns-page__create-button')
    TRAFFIC_TYPE = (By.XPATH, '//div[@class="column-list-item__title js-title"]')
    LINK_FIELD = (By.XPATH, '//div[@class="input input_create-main-url"]//input')
    NAME_FIELD = (By.XPATH, '//div[@class="input input_campaign-name input_with-close"]//input')
    BANNER = (By.ID, '192')
    UPLOAD_ELEMENT = (By.XPATH, '//div[@class="input__file-wrap"]/input')
    SAVE_PIC = (By.XPATH, '//input[@class ="image-cropper__save js-save"]')
    BUTTON_CREATE_CAMPAIGN = (By.XPATH, '//div[@class="footer"]//button[@class="button button_submit"]')

    BUTTON_SEGMENTS = (By.XPATH, '//a[contains(@href, "/segments")]')
    LINK_FIRST_SEGMENT = (By.XPATH, '//div[@class="instruction__wrap"]//a')
    BUTTON_CREATE_SEGMENT = (By.CLASS_NAME, 'button__text')
    ADD_SEGMENTS = (By.XPATH, '//span[@data-translated="Add audience segments..."]')
    OPTION_SEGMENT = (By.XPATH, '//div[contains(text(), "Приложения (ОК и МойМир)")]')
    FIRST_CHECKBOX = (By.XPATH, '//input[contains(@class, "adding-segments-source__checkbox js-main-source-checkbox")]')
    BUTTON_LIST = (By.XPATH, '//div[@class="adding-segments-source__text-top"]')
    SECOND_CHECKBOX = (By.XPATH, '//input[contains(@class, "segment-settings-view__checkbox js-payer-checkbox-pay")]')
    BUTTON_ADD_SEGMENT = (By.XPATH, '//div[@class="adding-segments-modal__btn-wrap js-add-button"]/button')
    SEGMENT_NAME_FIELD = (By.XPATH, '//div[@class="input input_create-segment-form"]//input')
    BUTTON_CONFIRM_SEGMENT = (By.XPATH, '//div[contains(text(), "Создать сегмент")]')
    SEGMENT_NAME = (By.XPATH, '//a[@class="adv-camp-cell adv-camp-cell_name"]')
    BUTTON_SORT = (By.XPATH, '//div[@data-group-id="created"]/span')
    SEARCH_SEGMENT = (By.XPATH, '//input[@data-translated-attr="placeholder"]')
    DELETE_BUTTON = (By.XPATH, '//span[@class="icon-cross"]')
    CONFIRM_DELETE = (By.XPATH, '//button[@class="button button_confirm-remove button_general"]')
    SEARCH_SUGGESTION = (By.XPATH, '//li[@class="suggester-ts__item"]')
    EMPTY_SUGGESTION = (By.XPATH, '//li[@class="suggester-ts__item_empty-text suggester-ts__item"]')
    SEGMENT_COUNTER = (By.XPATH, '//a[@href="/segments/segments_list"]//span[@class="left-nav__count js-nav-item-count"]')
    SUGGESTION_ID = (By.XPATH, '//span[contains(@class, "adv-camp-cell adv-camp-cell_name")]')
