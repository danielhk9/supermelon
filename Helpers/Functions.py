import os
import xlsxwriter
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import xlrd


def getAllSubAndMainCategories(driver):
    pCategories = findElementByXpath(driver,
                                     '//ul[@class="vertical-type sm-megamenu-hover sm_megamenu_menu sm_megamenu_menu_black"]')
    categories = getTagNames(pCategories, "li")
    return categories


def getAllSubAndMainServices(driver):
    pServices = findElementByXpath(driver,
                                   '//li[@class="services-parent other-toggle  sm_megamenu_lv1 sm_megamenu_drop parent  "]')
    services = getTagNames(pServices, "a")
    return services


def getTagNames(driver, tagName):
    element = driver.find_elements_by_tag_name(tagName)
    return element


def createExcelFile(fileName, sheetName, detect):
    wb = xlsxwriter.Workbook(fileName)
    ws = wb.add_worksheet(sheetName)
    bold = wb.add_format({'bold': 1})
    ws.write('A1', 'Product ID', bold)
    ws.write('B1', 'Image Name', bold)
    ws.write('C1', detect, bold)
    ws.write('D1', 'Image URL', bold)
    return [wb, ws]


def getTagName(driver, tagName):
    element = driver.find_element_by_tag_name(tagName)
    return element


def waitToThePageToLoad(driver):
    delay = 5
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'logged-in-mob')))
        return True
    except TimeoutException:
        return False


def focusOnMainCategory(driver, category):
    className = category.get_attribute("class")
    mainCategory = category.find_element_by_xpath(f"//li[@class='{className}']")
    ActionChains(driver).move_to_element(mainCategory).perform()
    text = category.text.split("\n")
    if text[0] == '':
        return False
    print(f'Focus on "{text[0]}" category')
    return mainCategory


def findElementsByClassName(driver, className):
    element = driver.find_elements_by_class_name(className)
    return element


def findElementByClassName(driver, className):
    element = driver.find_element_by_class_name(className)
    return element


def findElementByXpath(driver, xpath):
    # example -  '//span[@class="sm_megamenu_title_link"]
    try:
        element = driver.find_element_by_xpath(xpath)
        return element
    except NoSuchElementException:
        return False


def findElementsByXpath(driver, xpath):
    ##'//span[@class="sm_megamenu_title_link"]
    element = driver.find_elements_by_xpath(xpath)
    return element


def changeWindowAndSwitch(driver, num, text=None):
    if len(driver.window_handles) >= 2:
        window = driver.window_handles[num]
        driver.switch_to.window(window)
        if text:
            print(f'A new window opens after clicking on the "{text}" element')
        return window
    elif num == 0:  # in a case need to switch to the first window to
        window = driver.window_handles[num]
        driver.switch_to.window(window)
        print(f'Returned to the main window\n')
        return window
    else:
        print(f'No window was open after press on')
        return False


def clickAndOpenNewTab(driver, element):
    ActionChains(driver).key_down(Keys.COMMAND).click(element).perform()
    print(f'The "{element.text}" element is pressed')


def checkIfPopUpAppears(driver, popup, exitFromPopUp=None):
    driver.switch_to.parent_frame()
    if popup == 'login':
        if not findElementByXpath(driver, '//input[@title="Email"]'):
            return False
    elif popup == "enterprise":
        if not findElementByXpath(driver, '//div[@class="enterprise-popup"]'):
            return False
    closeButton = findElementsByXpath(driver, '//div[@data-role="closeBtn"]')
    n = 0
    if exitFromPopUp is None:
        while True:
            try:
                closeButton[n].click()
                break
            except ElementNotInteractableException:
                n += 1
        driver.switch_to.window(driver.window_handles[0])
    return True
