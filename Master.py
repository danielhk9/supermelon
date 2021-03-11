import unittest
from selenium import webdriver
from BeforeSignIn.AllCategories import CheckAllCategories
from BeforeSignIn.AllServices import CheckAllServices
from BeforeSignIn.Blog import CheckBlog
from BeforeSignIn.ReadyToShip import CheckReadyToShip
from BeforeSignIn.AboutUS import CheckAboutUs
from Helpers.Functions import changeWindowAndSwitch
from SignInAndOut.LoginToSite import LoginFeature
from AfterSignIn.UrlAndProducts import CheckAllProducts


class InitFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUpClass")
        cls.driver = webdriver.Chrome(executable_path='/Users/danielh/Downloads/chromedriver')
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        cls.driver.get("https://supermelon.com")

    def testAllCategories(self):
        print("test All Cate")
        results = CheckAllCategories(self.driver).pressOnEachCategory()
        self.assertEqual(results, True)

    def testAllServices(self):
        print("Services")
        results = CheckAllServices(self.driver).pressOnEachServices()
        self.assertEqual(results, True)

    def testReadyToShip(self):
        print("ready to ship")
        results = CheckReadyToShip(self.driver).pressOnReadyToShip()
        self.assertEqual(results, True)

    def testAboutUs(self):
        results = CheckAboutUs(self.driver).pressOnAboutUS()
        self.assertEqual(results, True)

    def testBlogScreen(self):
        results = CheckBlog(self.driver).pressOnBlog()
        self.assertEqual(results, True)

    def loginToSite(self):
        results = LoginFeature(self.driver).checkLoginInFeature()
        self.assertEqual(results, True)

    def testAllProducts(self):
        print('daniel')
        self.loginToSite()
        results = CheckAllProducts(self.driver).pressOnEachProduct()
        self.assertEqual(results, True)


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

    unittest.main()
