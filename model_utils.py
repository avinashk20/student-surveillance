import cv2
from deepface import DeepFace

import mongo_utils

MODEL = 'Facenet'
DETECTOR = 'dlib'

def getRepresentations(img):    # img = numpy array (BGR) or base64 encoded 
    try:
        obj = DeepFace.represent(
            img_path=img,
            model_name=MODEL,
            detector_backend=DETECTOR,
        )
        return obj
    except Exception:
        print('no face detected')
        return Exception

def getEmbedding(img):
    try:
        obj = getRepresentations(img)
        return obj[0]['embedding']
    except Exception:
       return Exception

def drawRectangle(img, facial_area):
    x = facial_area['x']
    y = facial_area['y']
    w = facial_area['w']
    h = facial_area['h']
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
    return img

def findSuspects(input_img):
    try:
        input_representations = getRepresentations(input_img)
        print('Detected', len(input_representations), 'face(s)')
        
        found_suspect_ids = []             # stores ids of matched suspects
        matched_rep_ids = []               # stores corresponding indexes of matched representations in input
        rep_index = 0
        for rep in input_representations:
            res = mongo_utils.findMatch(rep['embedding'])
            
            if(len(res) > 0):
                matched_rep_ids.append(rep_index)
                found_suspect_ids.append(res[0]['_id'])
                
            rep_index += 1
    
        # drawing a bounding box around found suspects
        suspects_img = input_img
        for id in matched_rep_ids:
            facial_area = input_representations[id]['facial_area']
            suspects_img = drawRectangle(suspects_img, facial_area)
              
        return {'found_suspect_ids': found_suspect_ids, 'suspects_img': suspects_img}
    
    except Exception:
        return Exception 

