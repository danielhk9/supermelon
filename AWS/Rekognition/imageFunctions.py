from collections import Counter

import PIL.Image
import cv2
import requests
from pytesseract import pytesseract
import os

from Helpers.Functions import createExcelFile
import shutil

import requests


def getSizeAndUnavailable():
    images = getAllImages()
    for image in images:
        if not image == '':
            productName = image.split(",")[0]
            imageName = image.split(",")[1]
            imageURL = f"https://supermelon.com/media/catalog/product{imageName}"
            # imagePath = saveTheImage(imageURL, imageName)
            # getUnavailableImages(imagePath)
            # getImageSize(imagePath)
            # deleteTheImage(imagePath)


def getImageSize(imagePath, productID, imageName, imageURL, ws1, num):
    image = PIL.Image.open(imagePath)
    width, height = image.size
    if 250 > width and 250 > height:
        print(f'The size of {imageName} image is less the 250')
        ws1.write(f'A{num}', productID)
        ws1.write(f'B{num}', imageName)
        ws1.write(f'C{num}', f"{width, height}")
        ws1.write(f'D{num}', imageURL)
        num += 1
    image.close()
    return num



def getUnavailableImages():
    excelFile = createExcelFile("Unavailable_images.xlsx", "unavailable images", "Detect Text")
    excelFile2 = createExcelFile("Image_Size.xlsx", "Size", "Size")
    wb = excelFile[0]
    ws = excelFile[1]
    wb1 = excelFile2[0]
    ws1 = excelFile2[1]
    startNum = 2
    num = 2
    s = 0
    images = getAllImages()
    try:
        for productID, allImages in images.items():
            s += 1
            print(s)
            if 6147 > s:
                print(s)
                continue
            for image in allImages:
                imageURL = f"https://supermelon.com/media/catalog/product/{image}"
                imageName = image.split("/")[-1]
                imagePath = saveTheImage(imageURL, imageName)
                img = cv2.imread(imagePath)
                try:
                    text = pytesseract.image_to_string(img)
                except TypeError:
                    ws.write(f'A{startNum}', productID)
                    ws.write(f'B{startNum}', imageName)
                    ws.write(f'C{startNum}', "Image not exits")
                    ws.write(f'D{startNum}', imageURL)
                    startNum += 1
                    deleteTheImage(imagePath)
                    continue
                if "No Image Available" in text:
                    print(f"{imageName} is unavailable")
                    ws.write(f'A{startNum}', productID)
                    ws.write(f'B{startNum}', imageName)
                    ws.write(f'C{startNum}', text)
                    ws.write(f'D{startNum}', imageURL)
                    startNum += 1
                newNum = getImageSize(imagePath, productID, imageName, imageURL, ws1, num)
                num = newNum
                deleteTheImage(imagePath)
    except Exception as e:
        print(e)
        print(imageURL)
        print(imageName)
        print(productID)
        print(s)
    finally:
        wb.close()
        wb1.close()
        return True


def getAllImages():
    images = {}
    with open(f'{os.getcwd()}/Files/ImagesName.csv') as names:
        names = names.read().splitlines()
    for name in names:
        if not name == '':
            productName = name.split(",")[0]
            imageName = name.split(",")[1]
            if productName in images.keys():
                if imageName in images[productName]:
                    continue
                newImageName = images[productName]
                newImageName.append(imageName)
                imageName = newImageName
                images.update({productName: imageName})
            else:
                images.update({productName: [imageName]})
    return images


def saveTheImage(imageURL, imageName):
    downloadTheImage = requests.get(imageURL)
    with open(imageName, 'wb') as outfile:
        outfile.write(downloadTheImage.content)
    outfile.close()
    imagePath = f'{os.getcwd()}/{imageName}'
    return imagePath


def deleteTheImage(imagePath):
    os.system(f"rm {imagePath}")
