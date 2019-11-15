import cv2
import boto3
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image


def dmc_detect(photo):
    Dmc = decode(Image.open(photo))

    if (len(Dmc) != 0) and (len(Dmc[0].data) > 0):
        print(Dmc[0].data.split('/')[4])
        return Dmc[0].data.split('/')[4]

    return ""


def upload_image_to_s3(img_name):
    s3 = boto3.resource('s3')

    data = open(img_name, 'rb')
    s3.Bucket('collinsoncards').put_object(Key='card.png', Body=data)


def process_image(bucket, photo):
    client = boto3.client('rekognition')

    return client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})


def process(photo, bucket, oldCard):
    dmcCard = dmc_detect(photo)
    if dmcCard != "":
        if dmcCard == oldCard:
            print('old')
        else:
            oldCard = dmcCard
            return dmcCard

    upload_image_to_s3(photo)
    response = process_image(bucket, photo)

    for text in response['TextDetections']:

        if (text['DetectedText'].isdigit()) and len(text['DetectedText']) == 10:
            if oldCard == text['DetectedText']:
                print('old card')
                break
            else:
                oldCard = text['DetectedText']
                return text['DetectedText']
        print('fail')


def main():
    cam = cv2.VideoCapture(0)
    img_name = "card.png"
    bucket = 'collinsoncards'
    oldCard = "card"

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

            if area > 400:
                if len(approx) == 4:
                    cv2.imwrite(img_name, frame)
                    card_number = process(img_name, bucket, oldCard)
                    if len(card_number) > 0:
                        cam.release()
                        return card_number


if __name__ == "__main__":
    main()
