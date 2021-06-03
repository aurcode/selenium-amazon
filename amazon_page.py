from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from time import sleep
import pandas as pd

class AmazonPage(object):
    def __init__(self, driver):
        self._driver = driver
        self._url = 'https://www.amazon.com/'
        self._delay = 60
        self.search_locator = 'field-keywords'
        self._select_country = 'nav-global-location-popover-link'
        self._country_button = 'a-button-text a-declarative'

    @property
    def is_loaded(self):
        WebDriverWait(self._driver, self._delay).until(EC.presence_of_element_located((By.NAME, self.search_locator)))
        return True

    @property
    def keyword(self):
        input_field = self._driver.find_element_by_name(self.search_locator)
        return input_field.get_attribute('value')

    def open(self):
        self._driver.get(self._url)
        print('\n\nOpen', self._url)
        sleep(2)

    def change_country(self, country):
        try:
            select_country = WebDriverWait(self._driver, self._delay).until(EC.presence_of_element_located((By.ID, self._select_country)))
            select_country.click()

            button_country = WebDriverWait(self._driver, self._delay).until(EC.element_to_be_clickable((By.XPATH, '//span[@class="a-button-text a-declarative"]')))
            button_country.click()

            list_country = WebDriverWait(self._driver, self._delay).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="a-popover-inner a-lgtbox-vertical-scroll"]/ul')))
            list_country = list_country.find_element_by_link_text(country)
            list_country.click()

            done = list_country = WebDriverWait(self._driver, self._delay).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="a-popover-3"]/div/div[2]/span/span/span/button')))
            done.click()
            print('Change country to', country)
        except TimeoutException:
            print('Change country, TimeoutException')

    def type_search(self, keyword):
        input_field = self._driver.find_element_by_name(self.search_locator)
        input_field.send_keys(keyword)

    def click_submit(self):
        input_field = self._driver.find_element_by_name(self.search_locator)
        input_field.submit()

    def filter_product(self, filter):
        s = WebDriverWait(self._driver, self._delay).until(EC.presence_of_element_located((By.XPATH, '//div[@class="a-section a-spacing-double-large"]')))
        s.find_element_by_xpath(f'.//span[.="{filter}"]').click()
        print(f'Apply filter "{filter}"')

    def sort_by(self, by):
        sort_list = WebDriverWait(self._driver, self._delay).until(EC.presence_of_element_located((By.XPATH, '//span[@class="a-button-text a-declarative"]')))
        sort_list.click()
        f = WebDriverWait(self._driver, self._delay).until(EC.presence_of_element_located((By.XPATH, '//div[@class="a-popover-inner"]/ul')))
        f.find_element_by_link_text(by).click()
        print(f'Sort by "{by}"')

    def add_to_dic(self, find_element, product):
        try:
            return find_element(product)
        except NoSuchElementException:
            return None


    def saving_elements(self):
        sleep(2)
        products = WebDriverWait(self._driver, self._delay).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="a-section a-spacing-medium"]//div[@class="sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20"]')))
        title = lambda a : a.find_element_by_xpath('.//h2/a/span').text
        price = lambda a : a.find_element_by_xpath('.//span[@class="a-price-whole"]').text
        ranking = lambda a: a.find_element_by_xpath('.//span[@class="a-size-base"]').text
        url = lambda a : a.find_element_by_xpath('.//a[@class="a-link-normal a-text-normal"]').get_attribute('href')
        list_products = []
        for product in products:
            dic = {}
            dic['title'] = self.add_to_dic(title, product)
            dic['price'] = self.add_to_dic(price, product)
            dic['ranking'] = self.add_to_dic(ranking, product)
            dic['url'] = self.add_to_dic(url, product)
            list_products.append(dic)

        df = pd.DataFrame(list_products)
        print(df)
            
        return df

    def search(self, keyword):
        self.type_search(keyword)
        self.click_submit()
        print(f'Search "{keyword}"')
