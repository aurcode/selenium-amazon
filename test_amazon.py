import unittest
from selenium import webdriver
from amazon_page import AmazonPage

class AmazonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(executable_path='../chromedriver')

    def test_search(self):
        amazon = AmazonPage(self.driver)
        amazon.open()
        amazon.change_country('Colombia')
        amazon.search('playstation 4')
        self.assertEqual('playstation 4', amazon.keyword)
        amazon.filter_product('New')
        amazon.filter_product('Include Out of Stock')
        amazon.sort_by('Price: High to Low')
        amazon.saving_elements()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__=='__main__':
    unittest.main(verbosity=2)