
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from Helpers.Functions import findElementByXpath, getAllSubAndMainServices, changeWindowAndSwitch, getTagName


class CheckAllServices:

    def __init__(self, driver):
        self.driver = driver
        self.lll = []

    def pressOnEachServices(self, checkSpelling=None):
        services = getAllSubAndMainServices(self.driver)
        findElementByXpath(self.driver, '//span[@data-horizontal-title="Services"]').click()
        for service in services:
            if service.text == '':  # some services with empty value
                break
            elif service.text == "Services" or "Quality" in service.text:  # this is the main service
                continue
            else:
                textInUrl = service.text.split()
                addToURL = ''
                # In case of error use this error:
                error = f'the service text was: {service.text}, It cannot be matched to the URL\nThe URL is {service.get_attribute("href")}'
                for text in textInUrl:
                    if f'#{text.lower()}' in service.get_attribute("href"):
                        addToURL = text
                        break
                if addToURL == '':
                    raise Exception(error)
                getDataForURL = findElementByXpath(service, '../../..')
                getDataForURL = getTagName(getDataForURL, "h2")
                addToURL2 = getDataForURL.text.replace(" ", '-')
                buildURL = f'https://supermelon.com/{addToURL2.lower()}#{addToURL.lower()}'
                if not addToURL2.lower() in self.lll:
                    ActionChains(self.driver).key_down(Keys.COMMAND).click(service).perform()
                    self.lll.append(addToURL2.lower())
                if checkSpelling:
                    changeWindowAndSwitch(self.driver, 0)
                    continue
                window2 = changeWindowAndSwitch(self.driver, 1, service.text)
                if not window2:
                    error = f'The button:{service.text} was not pressed'
                    raise Exception(error)
                if self.driver.current_url == buildURL:
                    self.driver.execute_script("window.close('');")
                    changeWindowAndSwitch(self.driver, 0)
                else:
                    self.driver.execute_script("window.close('');")
                    changeWindowAndSwitch(self.driver, 0)
                    raise Exception(error)
        return True
