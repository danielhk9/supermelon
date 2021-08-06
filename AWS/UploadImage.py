import boto3

import os
from AWS.Rekognition.ImageFunctions import saveTheImage, getAllImages, deleteTheImage, getImageSize
from AWS.Rekognition.DetectTextFromImage import detectText



def imageToAWS():
    s = 0
    uploadedImages = ''
    found = 'product id, image name, detect, image url(splithere)'
    aws_access_key_id = ""
    aws_secret_access_key = ""
    with open(f'{os.getcwd()}/Files/awsKeys') as code:
        keys = code.readline().split(",")
    clientS3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    clientRekognition = boto3.client('rekognition', region_name='us-east-2', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
    stop = False
    images = getAllImages()
    try:
        for productID, allImages in images.items():
            if stop:
                break
            for image in allImages:
                s += 1
                imagePath = f'{os.getcwd()}/Files/images/{image}'
                imageURL = f"https://supermelon.com/media/catalog/product/{image}"
                imageName = image.split('/')[-1]
                if imageName in uploadedImages:
                    if imageURL in found:
                        toAppend = f'{productID}, {imageName}, "image duplicate and already found in the file", {imageURL}(splithere)'
                        found = f'{found}{toAppend}'
                        print(s)
                        continue
                else:
                    if s > 1000:
                        clientS3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
                        clientS3.upload_file(imagePath, "supermelonbucket", imageName)
                    uploadedImages = uploadedImages.replace(uploadedImages, f'{uploadedImages},{imageName}')
                    text = detectText(clientRekognition, imageName)
                    if text:
                        toAppend = f'{productID}, {imageName}, {text}, {imageURL}(splithere)'
                        found = f'{found}{toAppend}'
                        if text == "Image not exits" or text == 'no image available':
                            deleteTheImage(imagePath)
                            print(s)
                            continue
                    size = getImageSize(imagePath)
                    if size:
                        toAppend = f'{productID}, {imageName}, {size}, {imageURL}(splithere)'
                        found = f'{found}{toAppend}'
                    deleteTheImage(imagePath)
                print(s)
                if s == 1000:
                    stop = True
                    break
    except Exception as e:
        print(e)
        print('finished')
    finally:
        f = found.split("(splithere)")
        for item in f:
            print(item)
            os.system(f'echo {item} >> file.txt')
    print('save the files')


def writeToExecl(ws, detect, imageName, productID, imageURL, num):
    print(f'Found {detect} on {imageName}')
    ws.write(f'A{num}', productID)
    ws.write(f'B{num}', imageName)
    ws.write(f'C{num}', detect)
    ws.write(f'D{num}', imageURL)
    num += 1
    return num
