import itertools
from Helpers.Functions import  findElementByXpath, findElementsByXpath, getTagName
import os

from SignInAndOut.LoginToSite import LoginFeature


class CheckAllProducts:
    def __init__(self, driver):
        self.driver = driver
        self.restartFunction = 0
        self.pages = 0
        self.numberOFTestedProducts = 0


    def pressOnEachProduct(self):
        with open(f"{os.getcwd()}/Files/newTest/allURLS.csv", "r") as file:
            urls = file.read().splitlines()
        for url in urls:
            self.driver.get(url)
            # numOfPages = findElementsByXpath(self.driver, '//span[@class="toolbar-number"]')
            # numOfPage = int(numOfPages[2].text) / 20
            # if not isinstance(numOfPage, int):
            #     numOfPage = int(numOfPage) + 1
            for num in itertools.count(start=1):
                if num > 5:
                    break
                url = url.replace(url, f'{url}?p={str(num)}')
                self.driver.get(url)
                products = findElementsByXpath(self.driver, '//div[@data-container="product-grid"]')
                for gg, product in enumerate(products):
                    productURL = getTagName(product, "a")
                    productURL = productURL.get_attribute("href")
                    self.driver.execute_script(f'''window.open("{productURL}","_blank");''')
                    if gg == 3:
                        break
                for number, window in enumerate(self.driver.window_handles):
                    if number > 0:
                        self.driver.switch_to.window(window)
                        if not "Hello," in findElementByXpath(self.driver, '//span[@class="logged-in"]').text:
                            LoginFeature(self.driver).checkLoginInFeature(skipOnSignInButton=True)
                        findElementByXpath(self.driver, '//a[@class="MagicZoom"]')
                        self.driver.execute_script("window.close('');")
                self.driver.switch_to.window(self.driver.window_handles[0])
                url = url.replace(f"?p={str(num)}", "")
                print("next page ----------------------")
            print('next url ---------------------------')
