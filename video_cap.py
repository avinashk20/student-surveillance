#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 15:17:27 2023

@author: avinash
"""

import monodb_test as model

import cv2
import threading
import matplotlib.pyplot as plt
import datetime
import pytz
import asyncio
import alert
import sys

IST = pytz.timezone('Asia/Kolkata')

ADDRESS = 'https://172.70.101.29:8080/video'

# ADDRESS = 'https://192.168.137.104:8080/video'
# ADDRESS1 = 'https://192.168.137.11:8080/video'

cap = cv2.VideoCapture(0)
cap.open(ADDRESS)

# cap1 = cv2.VideoCapture(0)
# cap1.open(ADDRESS1)

if not cap.isOpened():
    print("Error opening camera")
    sys.exit()

# if not cap1.isOpened():
#     print("Error opening camera")
#     exit()

window_width = 640
window_height = 480

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Camera", window_width, window_height)

# cv2.namedWindow("Camera1", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("Camera1", window_width, window_height)


def findMatch(frame):
    try:
        res = model.findSuspectsMongo(frame)
        found_suspects = res['found_suspects']
        modified_img = res['modified_img']

        num = len(found_suspects)

        if(num == 0):
            print('no match found')
            return

        print(num, 'matche(s) found')

        now = datetime.datetime.now(IST)
        timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

        print("At:", timestamp)
        print('--------found ids---------')
        print(found_suspects)
        print('--------------------------')
        plt.imshow(modified_img)
        plt.show()

        _, img_encoded = cv2.imencode('.jpg', modified_img)
        cam_image = img_encoded.tobytes()

        for suspect in found_suspects:
            student_data = model.getStudentDetails(suspect)
            
            caption = 'Student Name: {}\n Roll NO: {}\n Timestamp: {}'.format(
                student_data['name'], student_data['roll no'], timestamp)
            
            asyncio.run(alert.sendAlert(caption, suspect, cam_image))

        # return {'found_suspects': found_suspects,
        #         'modified_img': modified_img,
        #         'timestamp': timestamp
        #         }
    except Exception:
        pass


counter = 0

while True:
    ret, frame = cap.read()
    # ret1, frame1 = cap1.read()

    # if not ret or not ret1:
    #     print("Error reading frame from camera")
    #     break
    
    if not ret:
        print("Error reading frame from camera")
        break

    if(counter % 120 == 0):
        try:
            threading.Thread(target=findMatch, args=(frame.copy(),)).start()
            # threading.Thread(target=findMatch, args=(frame1.copy(),)).start()
        except Exception:
            print('error occured')

    counter += 1

    cv2.imshow('Camera', frame)
    # cv2.imshow('Camera1', frame1)

    # Press 'q' to exit
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
# cap1.release()
cv2.destroyAllWindows()
