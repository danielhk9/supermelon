import boto3
import unittest2
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from AWS.Rekognition.DetectLabelsFromImage import detectLabel
from AWS.Rekognition.ImageFunctions import getImageSize, getUnavailableImages, getSizeAndUnavailable

from AWS.UploadImage import imageToAWS
from AfterSignIn.UrlAndProducts import CheckAllProducts
from BeforeSignIn.AllCategories import CheckAllCategories
from BeforeSignIn.AllServices import CheckAllServices
from BeforeSignIn.Blog import CheckBlog
from BeforeSignIn.ReadyToShip import CheckReadyToShip
from BeforeSignIn.AboutUS import CheckAboutUs
#from BeforeSignIn.Spelling import CheckSpellingBeforeSignIn
from Helpers.Functions import changeWindowAndSwitch
from SignInAndOut.LoginToSite import LoginFeature
#from AfterSignIn.UrlAndProducts import CheckAllProducts
import os

from AWS.Rekognition.DetectTextFromImage import detectText


class InitFlow(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUpClass")
        options = Options()
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        cls.driver = webdriver.Chrome(executable_path=f'{os.getcwd()}/chromedriver', desired_capabilities=capabilities, options=options)
        # cls.driver.implicitly_wait(10)
        # cls.driver.maximize_window()
        # cls.driver.get("https://supermelon.com/")

    # def testAllCategories(self):
    #     print("test All Categories")
    #     results = CheckAllCategories(self.driver).pressOnEachCategory()
    #     self.assertEqual(results, True)
    #
    # def testAllServices(self):
    #     results = CheckAllServices(self.driver).pressOnEachServices()
    #     self.assertEqual(results, True)
    #
    # def testReadyToShip(self):
    #     results = CheckReadyToShip(self.driver).pressOnReadyToShip()
    #     self.assertEqual(results, True)
    #
    # def testAboutUs(self):
    #     results = CheckAboutUs(self.driver).pressOnAboutUS()
    #     self.assertEqual(results, True)
    #
    # def testBlogScreen(self):
    #     results = CheckBlog(self.driver).pressOnBlog()
    #     self.assertEqual(results, True)
    #
    # def loginToSite(self):
    #     results = LoginFeature(self.driver).checkLoginInFeature()
    #     self.assertEqual(results, True)
    #
    # def testAllProducts(self):
    #     self.loginToSite()
    #     results = CheckAllProducts(self.driver).pressOnEachProduct()
    #     self.assertEqual(results, True)
    #
    # def testSpelling(self):
    #     results = CheckSpellingBeforeSignIn(self.driver).getAllText()
    #     self.assertEqual(results, True)
    #
    # def testTextFromImages(self):
    #     results = DetectText(self.driver).checkImage("mysuper")
    #     self.assertEqual(results, True)
    #
    # def testLabelFromImages(self):
    #     results = DetectLabels(self.driver).checkLabel("mysuper")
    #     self.assertEqual(results, True)
    #
    # def testGetUnavailableImages(self):
    #     print("testing unavailable images")
    #     results = getUnavailableImages()
    #     self.assertEqual(results, True)

    # def testSizeOfImages(self):
    #     print("testing images size")
    #     results = getImageSize()
    #     self.assertEqual(results, True)

    def testAwsImageProcess(self):
        results = imageToAWS()
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
    unittest2.main()