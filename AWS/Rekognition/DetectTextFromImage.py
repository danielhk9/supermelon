
def detectText(clientRekognition, imageName):
    import botocore.exceptions
    stringToSearch = ['.ali', '.all', 'alibaba', '.com',
                      'coom', '.co', 'babo', 'bobo',
                      "com", "baba", "@", "www",
                      ".en", "..", ".,","abb","bala"]
    try:
        respond = clientRekognition.detect_text(Image={'S3Object': {'Bucket': "mysuper", "Name": imageName}})
    except botocore.exceptions.ClientError as e:
        return 'Image not exits'
    for num in range(len(respond["TextDetections"])):
        text = respond["TextDetections"][num]["DetectedText"].lower()
        match = [string for string in stringToSearch if string.lower() in text]
        if not "valeriano" in text and not "the " in text and match:
            return text
        if text == "no image available":
            return 'no image available'
    return False
