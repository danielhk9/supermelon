import pprint
from time import sleep

from Helpers.Functions import findElementByXpath, checkIfPopUpAppears

class LoginFeature:

    def __init__(self, driver):
        self.driver = driver

    def checkLoginInFeature(self, skipOnSignInButton=None):
        if not skipOnSignInButton:
            findElementByXpath(self.driver, '//a[@class="not-logged-in tg-click"]').click()
        if checkIfPopUpAppears(self.driver, 'login', exitFromPopUp=True):
            findElementByXpath(self.driver, '//input[@title="Email"]').clear()
            findElementByXpath(self.driver, '//input[@title="Email"]').send_keys("hakakdaniel@gmail.com")
            findElementByXpath(self.driver, '//input[@title="Password"]').send_keys("buzcan-6vuNpa-juwxyw")
            findElementByXpath(self.driver, '//a[@class="action login primary"]').click()
            sleep(10)
            return True
        else:
            raise Exception("Pop up login does not appear")

import json
def process_browser_logs_for_network_events(logs):
        for entry in logs:
            log = json.loads(entry["message"])["message"]
            if (
                    "Network.response" in log["method"]
                    or "Network.request" in log["method"]
                    or "Network.webSocket" in log["method"]
            ):
                yield log
