import boto3
import os
from AWS.Rekognition.ImageFunctions import saveTheImage, getAllImages, deleteTheImage, getImageSize
from AWS.Rekognition.DetectTextFromImage import detectText
from AWS.Rekognition.DetectLabelsFromImage import detectLabel
from Helpers.Functions import createExcelFile


def imageToAWS():
    excelFile1 = createExcelFile("Text.xlsx", "Detect Text", "Detect Text")
    textWb = excelFile1[0]
    textWs = excelFile1[1]
    excelFile2 = createExcelFile("Labels.xlsx", "Detect Labels", "Detect Labels")
    labelWb = excelFile2[0]
    labelWs = excelFile2[1]
    excelFile3 = createExcelFile("Image_Size.xlsx", "Size", "Size")
    sizeWb = excelFile3[0]
    sizeWs = excelFile3[1]
    s = 0
    startNumOfText = 2
    startNumOfLabel = 2
    startNumOfSize = 2
    with open(f'{os.getcwd()}/Files/awsKeys.csv') as code:
        keys = code.readline().split(",")
    clientS3 = boto3.client('s3', aws_access_key_id=keys[0], aws_secret_access_key=keys[1])
    clientRekognition = boto3.client('rekognition',  region_name='us-east-2', aws_access_key_id=keys[0], aws_secret_access_key=keys[1])
    images = getAllImages()
    try:
        for productID, allImages in images.items():
            s += 1
            print(s)
            for image in allImages:
                imageURL = f"https://supermelon.com/media/catalog/product/{image}"
                imageName = image.split('/')[-1]
                imagePath = saveTheImage(imageURL, imageName)
                clientS3.upload_file(imagePath, "mysuper", imageName)
                text = detectText(clientRekognition, imageName)
                if text:
                    startNumOfText = writeToExecl(textWs, text, imageName, productID, imageURL, startNumOfText)
                    if text == "Image not exits" or text == 'no image available':
                        deleteTheImage(imagePath)
                        continue
                label = detectLabel(clientRekognition, imageName)
                if label:
                    startNumOfLabel = writeToExecl(labelWs, label, imageName, productID, imageURL, startNumOfLabel)
                if s > 41277:
                    size = getImageSize(imagePath)
                    if size:
                        startNumOfSize = writeToExecl(sizeWs, size, imageName, productID, imageURL, startNumOfSize)
                deleteTheImage(imagePath)
    except Exception as e:
        print(e)
        print('finished')
    finally:
        print('save the files')
        textWb.close()
        labelWb.close()
        sizeWb.close()


def writeToExecl(ws, detect, imageName, productID, imageURL, num):
    print(f'Found {detect} on {imageName}')
    ws.write(f'A{num}', productID)
    ws.write(f'B{num}', imageName)
    ws.write(f'C{num}', detect)
    ws.write(f'D{num}', imageURL)
    num += 1
    return num
