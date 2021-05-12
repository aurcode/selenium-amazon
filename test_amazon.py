import unittest
from selenium import webdriver
from amazon_page import AmazonPage
from time import sleep

class AmazonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(executable_path='../chromedriver')

    def test_search(self):
        amazon = AmazonPage(self.driver)
        amazon.open()
        sleep(1)
        amazon.change_country('Colombia')
        #amazon.search('playstation 5')
        #self.assertEqual('playstation 5', amazon.keyword)
        #amazon.click_submit()
        sleep(60)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__=='__main__':
    unittest.main(verbosity=2)