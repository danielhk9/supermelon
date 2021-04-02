import boto3
from AWS.Rekognition.imageFunctions import saveTheImage, getAllImages, deleteTheImage


def UploadImageToAWS(buckets):
    with open(f'/Users/danielh/PycharmProjects/SuperMelon/Files/awsKeys') as code:
        keys = code.readline().split(",")
    clientS3 = boto3.client('s3', aws_access_key_id=keys[0], aws_secret_access_key=keys[1])
    names = getAllImages()
    for imageName in names:
        imageURL = f"https://supermelon.com/media/catalog/product{imageName}"
        imagePath = saveTheImage(imageURL, imageName)
        clientS3.upload_file(imagePath, buckets, imageName)
        print(f'was uploaded')
        deleteTheImage(imageURL)

