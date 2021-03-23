from time import sleep
from selenium.common.exceptions import NoSuchElementException
from Helpers.Functions import getAllSubAndMainCategories, findElementByXpath, findElementsByXpath, clickAndOpenNewTab, \
    getTagName, changeWindowAndSwitch, getTagNames


class CheckAllProducts:

    def __init__(self, driver):
        self.driver = driver
        self.restartFunction = 0
        self.pages = []
        self.numberOFTestedProducts = 0

    def pressOnEachProduct(self):
        browseButton = findElementByXpath(self.driver, '//a[@title="Browse Categories"]')
        if browseButton:
            browseButton.click()
        changeWindowAndSwitch(self.driver, 0)
        categories = getAllSubAndMainCategories(self.driver)
        for number, category in enumerate(categories):
            categoryName = category.get_attribute("class").split(" ")[0]
            print(f'Testing products on "{categoryName}" category')
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
        return True

    def switchAndClose(self, url):
        self.driver.execute_script(f'''window.open("{url}","_blank");''')
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.getAllUrlPages()
        self.clickOnItem()
        self.driver.execute_script("window.close('');")
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.pages.clear()

    def getAllUrlPages(self, checkSpelling=None):
        elementPages = findElementByXpath(self.driver, '//ul[@class="items pages-items"]')
        if not elementPages:
            self.pages.insert(0, "current")
            return self.pages
        pages = getTagNames(elementPages, "li")
        for page in pages:
            try:
                url = getTagName(page, "a")
                url = url.get_attribute("href")
                if not url in self.pages:
                    self.pages.append(url)
                else:
                    continue
            except NoSuchElementException:
                self.pages.insert(0, "current")
        return self.pages

    def clickOnItem(self):
        for pageNumber, page in enumerate(self.pages):
            if not pageNumber == 0:
                self.driver.get(page)
            element = findElementByXpath(self.driver, '//ol[@class="products list items product-items"]')
            elements = getTagNames(element, "li")
            className = elements[0].get_attribute("class")
            for numOFElement, element in enumerate(elements):
                self.numberOFTestedProducts += 1
                print(self.numberOFTestedProducts)
                el = findElementsByXpath(self.driver, f'//li[@class="{className}"]')
                getTheElement = getTagName(el[numOFElement], "a")
                url = getTheElement.get_attribute("href")
                print(f'Product number: {self.numberOFTestedProducts}')
                if not 'https://' in url:
                    name = getTagName(el[numOFElement], "strong").text
                    print(f'The url of {name} is:{url}')
                    continue
                print(url)
                self.driver.get(url)
                self.driver.back()
