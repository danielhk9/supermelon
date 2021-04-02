import json
import os
import sys
import urllib
from time import sleep

import PIL.Image
import boto3
import botocore

import urllib3
import xlrd
import xlsxwriter
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains

from AfterSignIn.UrlAndProducts import CheckAllProducts
from Helpers.Functions import findElementsByXpath, getTagNames, findElementByXpath, getTagName, findElementByClassName, \
    createExcelFile
import urllib.request as tr
import requests


class DetectText:

    def __init__(self, driver):
        self.driver = driver
        with open(f'{os.getcwd()}/awsKeys') as code:
            keys = code.readline().split(",")
        self.clientRekognition = boto3.client('rekognition', aws_access_key_id=keys[0], aws_secret_access_key=keys[1])
        self.ss = [151215, 72144, 93880, 73930, 404210, 73936, 64145, 404229, 1264594, 1264576, 1264575, 1264599,
                   404227, 1252144, 154755, 404226, 1264600, 1264577, 371317, 73004, 1264596, 1264574, 1264572, 1264548,
                   371562, 404235, 1264603, 73334, 187380, 1264604, 1264597, 1264542, 1264540, 404223, 404219, 211494,
                   211485, 1264606, 392791, 73932, 73216, 70649, 64264, 404220, 1264573, 258276, 187373, 180871, 145883,
                   73787, 71015, 1264544, 1264539, 371523, 371483, 371475, 187369, 70648, 64214, 1282952, 1282947,
                   1264593, 371723, 156977, 145841, 73212, 70659, 64163, 404232, 1264547, 1264541, 145604, 73786, 73289,
                   70656, 70655, 151239, 1364314, 1264546, 1264545, 371700, 371692, 371677, 371639, 371507, 371365,
                   187374, 187372, 156964, 73304, 73286, 70658, 64276, 404242, 93878, 371708, 371515, 371499, 371412,
                   371404, 371389, 163172, 151235, 139473, 70654, 70450, 64209, 404218, 182213, 154775, 73213, 70657,
                   1364347, 1184236, 404238, 404214, 371592, 371451, 187367, 145602, 73290, 73254, 404243, 187376,
                   145802, 404222, 371341, 371333, 187370, 154761, 1282953, 416298, 371623, 371467, 234917, 180890,
                   151172, 136100, 70956, 70651, 70650, 1230368, 1178847, 1155562, 371381, 64288, 1364346, 1322500,
                   1197096, 1155567, 145603, 1264602, 545479, 371459, 73218, 73210, 404239, 404234, 211486, 154778,
                   134807, 73916, 151237, 73277, 73231, 73211, 70660, 163188, 154760, 371577, 187378, 145605, 73521,
                   371491, 371615, 371539, 156958, 72618, 404245, 404237, 211484, 211487, 371631, 145837, 70653, 64174,
                   1264598, 916607, 258271, 242967, 234820, 187377, 1264477, 3126322, 1568627, 1322934, 211513, 211495,
                   73287, 71970, 1264601, 371547, 234916, 73522, 73380, 64142, 64139, 1364320, 211493, 71989, 180883,
                   145890, 70652, 187772, 404212, 371662, 234915, 73892, 73539, 73538, 64115, 64001, 71447, 404240,
                   371738, 258435, 211492, 211491, 145836, 73292, 70851, 371435, 404241, 404236, 403225, 371600, 154771,
                   154752, 73547, 64097, 234924, 73295, 404213, 371420, 211481, 211480, 404244, 371443, 234826, 211483,
                   61508, 777527, 73044, 416619, 777528, 404231, 234950, 234827, 211496, 172228, 545447, 404230, 140545,
                   61520, 73307, 772020, 70666, 3141717, 234769]

        self.startNum = 2


    def checkImage(self, nameOFBucket, imageID=None, imageURL=None):
        excelFile = createExcelFile("Results", "Detect Text")
        wb = excelFile[0]
        ws = excelFile[1]
        stringToSearch = ['.ali', '.all', 'al', 'alibaba', '.com', 'coom', '.co', 'babo', 'bobo', "com", "baba", "@",
                          "www", ".en", "..", ".,"]
        respond = self.clientRekognition.detect_text(Image={'S3Object': {'Bucket': nameOFBucket,
                                                                         "Name": self.ss}})
        for num in range(30):
            try:
                detectText = respond["TextDetections"][num]["DetectedText"].lower()
                match = [string for string in stringToSearch if string.lower() in detectText]
                print(f'Found alibaba on {imageID}')
                if not "valeriano" in detectText and not "the " in detectText and match:
                    print(f'Found alibaba on {imageID}')
                    ws.write(f'A{self.startNum}', imageID)
                    ws.write(f'B{self.startNum}', detectText)
                    ws.write(f'C{self.startNum}', imageURL)
                    self.startNum += 1
                    break
            except IndexError:
                break
        wb.close()
