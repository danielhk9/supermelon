
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from Helpers.Functions import findElementsByXpath, findElementByClassName, changeWindowAndSwitch, getTagName, \
    findElementByXpath, checkIfPopUpAppears


class CheckAboutUs:

    def __init__(self, driver):
        self.driver = driver

    def pressOnAboutUS(self):
        element = findElementByXpath(self.driver, '//span[@data-horizontal-title="About"]')
        ActionChains(self.driver).key_down(Keys.COMMAND).click(element).perform()
        errorAbout = f"about page does not appear after press on {element.text}\n the url was {self.driver.current_url}"
        window = changeWindowAndSwitch(self.driver, 1)
        if not window:
            errorButton = f'The button:{element.text} was not pressed'
            raise Exception(errorButton)
        if self.driver.current_url == "https://supermelon.com/about-us":
            sleep(2)
            startedButton = findElementByXpath(self.driver, '//a[@class="action button cms-signup-link"]')
            startedButton.click()
            if not checkIfPopUpAppears(self.driver, "enterprise"):
                error = f"login popup does not appear after press on {startedButton.text}\n"
                raise Exception(error)
        else:
            self.driver.execute_script("window.close('');")
            changeWindowAndSwitch(self.driver, 0)
            raise Exception(errorAbout)


        return True
