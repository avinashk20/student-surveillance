import cv2
import pytz

import threading
import sys
import time
from io import BytesIO

import model_utils
import mongo_utils
import telegram_utils


TIME_ZONE = pytz.timezone('Asia/Kolkata')

def check_frame(frame):
    try:
        res = model_utils.findSuspects(frame)
        found_suspect_ids = res['found_suspect_ids']
        suspects_img = res['suspects_img']

        num_suspects = len(found_suspect_ids)

        if(num_suspects == 0):
            print('no match found')
            return

        print(num_suspects, 'matche(s) found')

        timestamp = time.strftime("%d/%m/%Y %H:%M:%S")

        print("At:", timestamp)
        print('\n--------found ids---------')
        print(found_suspect_ids)
        print('--------------------------\n')

        _, img_encoded = cv2.imencode('.jpg', suspects_img)     # encoding the suspects image to jpeg 
        img_bytes = img_encoded.tobytes()                       # converting it to bytes for telegram alert
        
        telegram_utils.send_alert('Found suspects', BytesIO(img_bytes))
        
        suspects_details = mongo_utils.getSuspectsDetails(found_suspect_ids)
        
        for suspect in suspects_details:
            caption = 'Student Name: {}\n Student Id: {}\n Branch: {}\n Found At: {}\n'.format(
                suspect['name'],
                suspect['studentId'], 
                suspect['branch'], 
                timestamp
            )
            print(caption)
            telegram_utils.send_alert(caption, suspect['photoUrl'])

    except Exception:
        pass


SOURCE_ADDRESS = 

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

cap = cv2.VideoCapture(0)
cap.open(SOURCE_ADDRESS)

if not cap.isOpened():
    print("Error opening camera")
    sys.exit()

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Camera", WINDOW_WIDTH, WINDOW_HEIGHT)


WAIT_DURATION = 4               # check frame for every 4 seconds
FRAME_RATE = 30                 # video frame rate 30fps

target_frame = WAIT_DURATION * FRAME_RATE
frame_counter = 0
# loop_wait = 1 / FRAME_RATE

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error in reading frame from camera")
        break

    if(frame_counter % target_frame == 0):
        try:
            threading.Thread(target=check_frame, args=(frame.copy(),), daemon=True).start()
        except Exception as e:
            # pass 
            print(f'Error in creating new thread: {e}')

    frame_counter += 1

    cv2.imshow('Camera', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) == ord('q'):
        break
    
    # time.sleep(loop_wait)

cap.release()
cv2.destroyAllWindows()
