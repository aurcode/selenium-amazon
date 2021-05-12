from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class AmazonPage(object):
    def __init__(self, driver):
        self._driver = driver
        self._url = 'https://www.amazon.com/'
        self.search_locator = 'field-keywords'
        self._select_country = 'nav-global-location-popover-link'
        self._country_button = 'a-button-text a-declarative'

    @property
    def is_loaded(self):
        WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.NAME, self.search_locator)))
        return True

    @property
    def keyword(self):
        input_field = self._driver.find_element_by_name(self.search_locator)
        return input_field.get_attribute('value')

    def open(self):
        self._driver.get(self._url)

    def change_country(self, country):
        select_country = WebDriverWait(self._driver, 15).until(EC.element_to_be_clickable((By.ID, self._select_country)))
        select_country.click()
        sleep(3)
        country_button = Select(WebDriverWait(self._driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, self._country_button))))
        [print(option.text) for option in country_button.options]
        #country_button = self._driver.find_element_by_class_name(self._country_button)
        country_button.select_by_visible_text(country)
        #self._driver.find_element_by_name('glowDoneButton').click()
        #WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/gallery/"]')))

    def type_search(self, keyword):
        input_field = self._driver.find_element_by_name(self.search_locator)
        input_field.send_keys(keyword)

    def click_submit(self):
        input_field = self._driver.find_element_by_name(self.search_locator)
        input_field.submit()

    def search(self, keyword):
        self.type_search(keyword)
        self.click_submit