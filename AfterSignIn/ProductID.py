import os
from time import sleep

import xlsxwriter
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException

from Helpers.Functions import findElementsByXpath, findElementByXpath, getTagNames, getTagName, clickAndOpenNewTab, \
    changeWindowAndSwitch


class getAllProductID:
    workbook = xlsxwriter.Workbook(f'done.xlsx')


    def __init__(self, driver):
        self.driver = driver
        self.url = ''
        self.again = True

    def returnID(self):
        findElementByXpath(self.driver, '//input[@id="username"]').send_keys("categoryaccess")
        findElementByXpath(self.driver, '//input[@id="login"]').send_keys("Koshita1234#$%")
        el = findElementByXpath(self.driver, '//button[@class="action-login action-primary"]')
        el.click()
        n = 2
        element = findElementsByXpath(self.driver, '//li[@class="x-tree-node"]')
        sssss = element[n]
        n2 = 0
        name = ''
        here = True
        while True:
            element = findElementsByXpath(self.driver, '//li[@class="x-tree-node"]')
            if here:
                sssss = element[n]
            else:
                for na, s in enumerate(element):
                    if name == getTagName(s, "a").text:
                        sssss = element[na + 1]
                        here = True
                        break
            restart = True
            while restart:
                div = getTagName(sssss, 'div')
                if not "x-tree-node-leaf" in div.get_attribute("class"):
                    print(div.get_attribute("class"))
                    img = getTagNames(div, "img")
                    for i in img:
                        print(i.get_attribute("class"))
                        if "plus" in i.get_attribute("class"):
                            ul = getTagName(sssss, "ul")
                            restart2 = True
                            while restart2:
                                try:
                                    i.click()
                                    restart2 = False
                                except ElementClickInterceptedException as e:
                                    sleep(5)
                            sssss = ul
                            break
                        elif "minu" in i.get_attribute("class"):
                            ul = getTagName(sssss, "ul")
                            sssss = ul
                            break
                        else:
                            continue
                elif "x-tree-node-leaf" in div.get_attribute("class"):
                    l1 = getTagNames(sssss, "li")
                    l1[n2].click()
                    self.url = self.driver.current_url
                    restart = False
            if self.again:
                self.press()
            else:
                self.workbook.close()
                break

    def press(self):
        allIDS = [5412]
        n = 1
        urlS = self.url.split("/id/")
        for id in allIDS:
            otherURL = f"{urlS[0]}/id/{id}"
            self.driver.get(otherURL)
            ssss111 = findElementByXpath(self.driver, '//div[@class="page-actions-inner"]')
            name = ssss111.get_attribute("data-title")
            name = name.split(" (")
            name = name[0]
            worksheet = self.workbook.add_worksheet(name)
            worksheet.write(0, 0, "product name")
            worksheet.write(0, 1, "sku")
            restart3 = True
            while restart3:
                try:
                    elementList = findElementByXpath(self.driver, '//ul[@class="product-list ui-sortable"]')
                    pressOnShowMore = True
                    products = getTagNames(elementList, "li")
                    restart3 = False
                except AttributeError as e:
                    self.driver.get(otherURL)
                    sleep(20)
            n3333 = 0
            while True:
                for pro in products:
                    n3333 += 1
                    if "automatic-sorting" in pro.get_attribute("class"):
                        pressOnShowMore = False
                        break
                    else:
                        getProdID = getTagNames(pro, "div")
                        for i in getProdID:
                            if i.get_attribute("class") == "info":
                                prodID = getTagNames(pro, "p")
                                for product in prodID:
                                    if product.get_attribute("class") == "sku":
                                        sku = product.text
                                        prodName = getTagName(pro, "h1")
                                        worksheet.write(n, 0, prodName.text)
                                        worksheet.write(n, 1, sku)
                                        n += 1
                                        break


                if pressOnShowMore:
                    print("the product have more name")
                break
        self.again = False

                # ul = getTagName(element[n],"ul")
                # subC = getTagName(ul, "li")
                # ul = getTagName(subC, "ul")
                # img = getTagNames(ul, "img")
                # for a in img:
                #     if a.get_attribute("class") == "x-tree-ec-icon x-tree-elbow-plus":
                #         a.click()
                # subC1 = getTagNames(ul, "li")
                # print(len(subC1))
                # for sub in subC:
                #     print(sub.get_attribute("class"))
                #     if expended in sub.get_attribute("class"):
                #         print(div.get_attribute("class"))
                #         img = getTagNames(div, "img")
                #         for i in img:
                #             if i.get_attribute("class") == "x-tree-ec-icon x-tree-elbow-plus":
                #                 i.click()
                #
                #             print(ul.get_attribute("class"))
                #
                # else:
                #     els = getTagName(div, "a")
                #     fileName = els.text.split(" (")
                #     name = fileName[0]
                #     print(name)
                #     while True:
                #         try:
                #             els.click()
                #             break
                #         except ElementNotInteractableException as e:
                #             self.driver.execute_script("window.scrollTo(0, 50)")
                #     elementList = findElementByXpath(self.driver,'//ul[@class="product-list ui-sortable"]')
                #     products = getTagNames(elementList, "li")
                #     for pro in products:
                #         if "automatic-sorting" in pro.get_attribute("class"):
                #             print(pro.get_attribute("class"))
                #             break
                #         else:
                #             getProdID = getTagNames(pro, "div")
                #             for i in getProdID:
                #                 print(i.get_attribute("class"))
                #                 if i.get_attribute("class") == "info":
                #                     prodID = getTagNames(pro, "p")
                #                     for product in prodID:
                #                         print(product.get_attribute("class"))
                #                         if product.get_attribute("class") == "sku":
                #                             print(name, product.text)
                #                             break
                #
                #


def getAllImages():
    images = {}
    with open("/Users/danielh/PycharmProjects/SuperMelon/categories-july28-2.csv") as file:
        names = file.read().splitlines()
    for name in names:
        name = name.split(",")
        images.update({name[3]: name[0]})
    return images
