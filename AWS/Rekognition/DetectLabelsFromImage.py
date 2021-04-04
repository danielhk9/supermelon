from colordict import ColorDict


def detectLabel(clientRekognition, imageName):
    colors = ColorDict()
    respond = clientRekognition.detect_labels(Image={'S3Object': {'Bucket': "mysuper", "Name": imageName}})
    for num in range(len(respond["Labels"])):
        label = respond["Labels"][num]["Name"].lower()
        if label == 'white' or label == "green" or label == "black" or \
                label == "gray" or label == "red" or label == "blue":
            color = colors[label]
            detectConfidence = respond["Labels"][num]["Confidence"]
            if detectConfidence > 70:
                return label
    return False
