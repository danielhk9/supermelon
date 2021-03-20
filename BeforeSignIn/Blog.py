
from Helpers.Functions import findElementsByXpath, changeWindowAndSwitch, findElementByXpath, getTagNames, \
    clickAndOpenNewTab


class CheckBlog:

    def __init__(self, driver):
        self.driver = driver

    def pressOnBlog(self, checkSpelling=None):
        element = findElementByXpath(self.driver, '//span[@data-horizontal-title="Blog"]')
        if element:
            clickAndOpenNewTab(self.driver, element)
        window = changeWindowAndSwitch(self.driver, 1)
        if not window:
            errorButton = f'The button:{element.text} was not pressed'
            raise Exception(errorButton)
        if self.driver.current_url == "https://supermelon.com/blog":
            listCategories = findElementByXpath(self.driver, '//ul[@class="list-categories"]')
            categories = getTagNames(listCategories, 'li')
            for category in categories:
                clickAndOpenNewTab(self.driver, category)
                if checkSpelling:
                    continue
                textToSearch = category.text
                changeWindowAndSwitch(self.driver, 2)
                posts = findElementsByXpath(self.driver, '//div[@class="item post-categories"]')
                for post in posts:
                    if textToSearch == post.text:
                        self.driver.execute_script("window.close('');")
                        changeWindowAndSwitch(self.driver, 1)
                        break
                    else:
                        error = f"{textToSearch} web does not appear after press on {textToSearch}\n, the url is: {self.driver.current_url}"
                        raise Exception(error)
        return True


