from Helpers.Functions import findElementByXpath, checkIfPopUpAppears

class LoginFeature:

    def __init__(self, driver):
        self.driver = driver

    def checkLoginInFeature(self):
        findElementByXpath(self.driver, '//a[@class="not-logged-in tg-click"]').click()
        if checkIfPopUpAppears(self.driver, 'login', exitFromPopUp=True):
            findElementByXpath(self.driver, '//input[@title="Email"]').send_keys("hakakdaniel@gmail.com")
            findElementByXpath(self.driver, '//input[@title="Password"]').send_keys("super543&")
            findElementByXpath(self.driver, '//a[@class="action login primary"]').click()
            return True
        else:
            raise Exception("Pop up login does not appear")




