import cv2
import boto3
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image


cam = cv2.VideoCapture(1)
card = ""
font = cv2.FONT_HERSHEY_COMPLEX
img_name = "card.png"
card = ""
bucket = 'collinsoncards'
photo = 'card.png'
oldCard = "card"


def dmc_detect():
    Dmc = decode(Image.open(photo))

    if (len(Dmc) != 0) and (len(Dmc[0].data) > 0):
        print Dmc[0].data.split('/')[4]
        return Dmc[0].data.split('/')[4]

    return ""


def upload_image_to_s3():
    s3 = boto3.resource('s3')

    data = open(img_name, 'rb')
    s3.Bucket('collinsoncards').put_object(Key='card.png', Body=data)


def process_image():
    client = boto3.client('rekognition')

    return client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})


def process():

    global oldCard
    dmcCard = dmc_detect()
    if dmcCard != "":
        if dmcCard == oldCard:
            print 'old'
        oldCard = dmcCard
        return dmcCard

    upload_image_to_s3()
    response = process_image()

    for text in response['TextDetections']:

        if (text['DetectedText'].isdigit()) and len(text['DetectedText']) == 10:
            if oldCard == text['DetectedText']:
                print 'old card'
                break
            else:
                oldCard = text['DetectedText']
                print text['DetectedText']
                return text['DetectedText']
            print 'fail'

while True:
    ret, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 48, 13])
    upper_red = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if area > 400:
            #cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
            if len(approx) == 4:
                cv2.imwrite(img_name, frame)
                process()

        cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
cam.release()

cv2.destroyAllWindows()

