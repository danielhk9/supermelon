from Helpers.Functions import getAllSubAndMainCategories, findElementByXpath, findElementsByXpath

class CheckAllCategories:

    def __init__(self, driver):
        self.driver = driver

    def pressOnEachCategory(self):
        categories = getAllSubAndMainCategories(self.driver)
        for number, category in enumerate(categories):
            print(category.get_attribute("class"))
            if "popularcategories" in category.get_attribute("class"):
                subCategories = findElementsByXpath(category, '//span[@class="sm_megamenu_title_link"]')
            else:
                subCategories = findElementsByXpath(category, '//span[@class="sm_megamenu_title_lv-2"]')
            for number2, subCategory in enumerate(subCategories):
                getParentElement = findElementByXpath(subCategory, "..")
                className = getParentElement.get_attribute("class")
                if not "show-popup-signup" in className:
                    print(className)
                    print(getParentElement.text)
                    error = f"login popup does not belongs to the element, the class name is: {className}\n"
                    raise Exception(error)
        return True

