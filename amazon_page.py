from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
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
        sleep(5)

    def change_country(self, country):
        select_country = WebDriverWait(self._driver, 15).until(EC.element_to_be_clickable((By.ID, self._select_country)))
        select_country.click()
        sleep(3)

        button_country = self._driver.find_element_by_xpath('//span[@class="a-button-text a-declarative"]')
        button_country.click()
        sleep(1)

        list_country = self._driver.find_element_by_xpath('//div[@class="a-popover-inner a-lgtbox-vertical-scroll"]/ul')
        list_country = list_country.find_element_by_link_text(country)
        list_country.click()
        sleep(3)

        done = self._driver.find_element_by_xpath('//div[@id="a-popover-3"]/div/div[2]/span/span/span/button')
        done.click()

    def type_search(self, keyword):
        input_field = self._driver.find_element_by_name(self.search_locator)
        input_field.send_keys(keyword)

    def click_submit(self):
        input_field = self._driver.find_element_by_name(self.search_locator)
        input_field.submit()

    def filter_product(self, f):
        s = self._driver.find_element_by_xpath('//div[@class="a-section a-spacing-double-large"]')
        s.find_element_by_xpath(f'//span[.="{f}"]').click()
        sleep(3)

    def sort_by(self, by):
        sort_list = self._driver.find_element_by_xpath('//span[@class="a-button-text a-declarative"]')
        sort_list.click()
        f = self._driver.find_element_by_xpath('//div[@class="a-popover-inner"]/ul')
        f.find_element_by_link_text(by).click()

    def view_price(self):
        products = self._driver.find_elements_by_xpath('//div[@class="a-section a-spacing-medium"]//div[@class="sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20"]')
        title = lambda a : a.find_element_by_xpath('.//h2/a/span').text
        price = lambda a : a.find_element_by_xpath('.//a[@class="a-size-base a-link-normal a-text-normal"]/span/span/span[@class="a-price-whole"]').text
        for product in products:
            try:
                if price(product):
                    print('Title:', title(product))
                    print(f'Price: ${price(product)}')
                    print('')
            except NoSuchElementException as e:
                pass

    def search(self, keyword):
        self.type_search(keyword)
        self.click_submit()
