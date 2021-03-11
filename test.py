import json
#import boto3
#
# from selenium.webdriver.chrome.remote_connection import ChromeRemoteConnection
#
#
# def uploadImage(photo):
#     client = boto3.client('rekognition', region_name='us-west-2')
#
#     with open(photo, 'rb') as image:
#         respond = client.detect_labels(Image={'Bytes': image.read()})
#
#         data = {
#             'source': photo,
#             'data': respond.get('Labels')
#         }
#
#         return json.dumps(data, indent=4)

import language_check
def ss():
    tool = language_check.LanguageTool('en-US')
    text = u'Your payment is safe with us. Supermelon holds your payment in escrow and will provide you with a full refund in the event that:1. You don’t receive your order 2. You receive the wrong item. 3. The product(s) you ordered are not as described. '
    matches = tool.check(text)
    for s in matches:
        print(s)



if __name__ == '__main__':
    #print(uploadImage("/Users/danielh/Downloads/220px-Florida_Driver_License.png"))
    ss()