#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 15:59:54 2023

@author: avinash
"""

# !pip install deepface cmake dlib

from PIL import Image
from io import BytesIO
import base64
from deepface import DeepFace
import numpy as np
import matplotlib.pyplot as plt
import cv2

# img = numpy array(BGR) or base64 or img_path

def encodeImage(img_path):
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string   

def decodeImage(base64Img):
    img = base64.b64decode(base64Img)
    pil_image = Image.open(BytesIO(img))
    return np.array(pil_image)

def getRepresentations(img):
    if(isinstance(img, bytes)):
        img = decodeImage(img)
    try:
        obj = DeepFace.represent(
            img_path=img,
            model_name='Facenet',
            detector_backend='dlib',
        )
        return obj
    except Exception:
        print('no face detected')
        return Exception
    

def getSuspectEmbedding(img):
    obj = getRepresentations(img)
    return obj[0]['embedding']


# find match

THREESHOLD_VALUE = 0.5  # facenet


def findCosineDistance(vector_1, vector_2):
    a = np.matmul(np.transpose(vector_1), vector_2)
    b = np.matmul(np.transpose(vector_1), vector_1)
    c = np.matmul(np.transpose(vector_2), vector_2)
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))


# suspects_embeddings = [{id, embedding}, ...]

def findSuspects(input_img, suspects_embeddings):
    input_representations = getRepresentations(input_img)
    found_suspects = []  # ids of matched suspects
    matched_reps = []  # ids of matched faces in input
    i = 0
    for rep in input_representations:
        for suspect in suspects_embeddings:
            distance = findCosineDistance(
                suspect['embedding'], rep['embedding'])
            if distance < THREESHOLD_VALUE:
                found_suspects.append(suspect['id'])
                matched_reps.append(i)
        i = i+1

    # show bounding box around found suspects

    # if base64Img

    if(isinstance(input_img, bytes)):
        img = decodeImage(input_img)

    # if numpy array

    elif(isinstance(input_img, np.ndarray)):
        img = input_img

    # if path
    else:
        img = plt.imread(input_img)

    for id in matched_reps:
        facial_area = input_representations[id]['facial_area']
        x = facial_area['x']
        y = facial_area['y']
        w = facial_area['w']
        h = facial_area['h']
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

    return {'found_suspects': found_suspects, 'modified_img': img}
