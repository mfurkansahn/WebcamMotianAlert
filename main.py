import glob
import os

import cv2
import time
import numpy as np

from emailing import send_email

from threading import Thread

kernel = np.ones((3, 3), np.uint8)

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None

status_list = []

count = 0


def clean_folder():
    print("clean_folder function started")
    images = glob.glob("images/*.jpg")
    for image in images:
        os.remove(image)
    print("clean_folder function ended")

while True:
    status = 0
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21,21), 0)
    # cv2.imshow("Gray and Blur Video", gray_frame)

    if first_frame is None:
        first_frame = gray_frame_gau
        # cv2.imshow("First Frame", frame)

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    # cv2.imshow("Delta Frame", delta_frame)
    # print(delta_frame)

    thresh_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow("Thresh Frame", thresh_frame)
    dil_frame = cv2.dilate(thresh_frame, kernel, iterations=2)
    cv2.imshow("Dilate Frame", dil_frame) #

    contours, check = cv2.findContours(dil_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y+ h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.jpg", frame)
            count += 1
            all_images = glob.glob(f"images/*.jpg")
            index = int(len(all_images)/2)
            image_with_object = all_images[index]



    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0 and image_with_object is not None:
        email_thread = Thread(target=send_email, args=(image_with_object,))
        email_thread.daemon = True
        email_thread.start()

        # clean_thread = Thread(target=clean_folder)
        # clean_thread.daemon = True
        # clean_thread.start()


    print(status_list)


    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()

clean_folder()

