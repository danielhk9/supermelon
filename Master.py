import unittest2
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import pytest
from BeforeSignIn.AllCategories import CheckAllCategories
from BeforeSignIn.AllServices import CheckAllServices
from BeforeSignIn.Blog import CheckBlog
from BeforeSignIn.ReadyToShip import CheckReadyToShip
from BeforeSignIn.AboutUS import CheckAboutUs
from Helpers.Functions import changeWindowAndSwitch, findElementsByXpath
from SignInAndOut.LoginToSite import LoginFeature
from AfterSignIn.UrlAndProducts import CheckAllProducts
import os
from pyvirtualdisplay import Display

class InitFlow(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUpClass")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        cls.driver = webdriver.Chrome(executable_path=f'{os.getcwd()}/chromedriver', desired_capabilities=capabilities,chrome_options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        cls.driver.get("https://supermelon.com/")

    def testAllCategories(self):
        print("test All Cate")
        assert CheckAllCategories(self.driver).pressOnEachCategory() is True

    def testAllServices(self):
        results = CheckAllServices(self.driver).pressOnEachServices()
        self.assertEqual(results, True)

    def testReadyToShip(self):
        assert CheckReadyToShip(self.driver).pressOnReadyToShip() is True

    def testAboutUs(self):
        assert CheckAboutUs(self.driver).pressOnAboutUS() is True

    def testBlogScreen(self):
        assert CheckBlog(self.driver).pressOnBlog() is True

    def loginToSite(self):
        assert LoginFeature(self.driver).checkLoginInFeature() is True

    # def testAllProducts(self):
    #     self.loginToSite()
    #     results = CheckAllProducts(self.driver).pressOnEachProduct()
    #     self.assertEqual(results, True)
    #
    # def testSpelling(self):
    #     results = CheckSpellingBeforeSignIn(self.driver).getAllText()
    #     self.assertEqual(results, True)

    def tearDown(self):
        while True:
            if len(self.driver.window_handles) >= 2:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.execute_script("window.close('');")
            else:
                changeWindowAndSwitch(self.driver, 0)
                break

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")
        cls.driver.close()
        cls.driver.quit()
        print("Test Completed")


if __name__ == '__main__':
    unittest2.main()
