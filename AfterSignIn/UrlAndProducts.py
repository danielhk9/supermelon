import concurrent.futures
import time
from time import sleep
import os

from Helpers.Functions import getAllSubAndMainCategories, findElementByXpath, findElementsByXpath, clickAndOpenNewTab, \
    getTagName, changeWindowAndSwitch, getTagNames, getAllSubAndMainReadyTOShip, focusOnMainCategory, getTagNameEX


class CheckAllProducts:

    def __init__(self, driver):
        self.driver = driver
        self.restartFunction = 0
        self.pages = 0
        self.numberOFTestedProducts = 0

    def pressOnEachProduct(self):
        os.system("touch allURLS.txt")
        changeWindowAndSwitch(self.driver, 0)
        categories = getAllSubAndMainCategories(self.driver)
        for number, category in enumerate(categories):
            print(category.get_attribute("class"))
            if "popularcategories" in category.get_attribute("class"):
                subCategories = findElementsByXpath(category, '//span[@class="sm_megamenu_title_link"]')
            else:
                subCategories = findElementsByXpath(category, '//span[@class="sm_megamenu_title_lv-2"]')
            for number2, subCategory in enumerate(subCategories):
                getParentElement = findElementByXpath(subCategory, "..")
                url = getParentElement.get_attribute("href")
                if url == "javascript:void(0)":
                    if self.restartFunction == 3:
                        raise Exception("Loading took too much time!")
                    sleep(2)
                    self.pressOnEachProduct()
                    self.restartFunction += 1
                self.switchAndClose(url)
                break
        return True

    def switchAndClose(self, url):
        for num in range(10, 61):
            print(f"page number {num}")
            url = url.replace(url, f'{url}?p={str(num)}')
            self.driver.execute_script(f'''window.open("{url}","_blank");''')
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.clickOnItem(num)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.execute_script("window.close('');")
            self.driver.switch_to.window(self.driver.window_handles[0])
            url = url.replace(f'?p={str(num)}', "")


    def clickOnItem(self,num):
        element = findElementByXpath(self.driver, '//ol[@class="products list items product-items"]')
        elements = getTagNames(element, "li")
        el = findElementsByXpath(self.driver, '//div[@class="productLbl"]')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.process_image, elements, el)
        for numberWin, window in enumerate(self.driver.window_handles):
            if numberWin > 1:
                self.driver.switch_to.window(window)
                imagesParent = findElementsByXpath(self.driver, '//div[@class="mcs-item"]')
                for image in imagesParent:
                    sumImage = getTagName(image, "a")
                    imageURL = sumImage.get_attribute("href")
                    os.system(f"echo {imageURL}, {str(num)} >> allURLS.txt")
                self.driver.execute_script(f'''window.close();''')

    def process_image(self, element, el):
        self.numberOFTestedProducts += 1
        if el.text == "":
            getTheElement = getTagName(element, "a")
            url = getTheElement.get_attribute("href")
            self.pages +=1
            self.driver.execute_script(f'''window.open("{url}","_blank");''')
