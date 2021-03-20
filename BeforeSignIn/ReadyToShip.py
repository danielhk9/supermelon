from Helpers.Functions import findElementByXpath, checkIfPopUpAppears, clickAndOpenNewTab, changeWindowAndSwitch


class CheckReadyToShip:

    def __init__(self, driver):
        self.driver = driver

    def pressOnReadyToShip(self, checkSpelling=None):
        print(self.driver.window_handles)
        element = findElementByXpath(self.driver, '//span[@data-horizontal-title="Ready to Ship"]')
        element.click()
        if not checkIfPopUpAppears(self.driver, "login"):
            error = f"login popup does not appear after press on {element.text}\n"
            raise Exception(error)
        return True
