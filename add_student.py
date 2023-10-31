#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 21:55:02 2023

@author: avinash
"""

import model
from pymongo import MongoClient

url = 'mongodb+srv://admin-avinash:ZV8SiWqsTzmkYo1S@cluster0.stfqxq6.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(url)

db = client.suspectsDB

mycol = db['students']

img_path = 'students/tanvir.jpeg'
embedding = model.getSuspectEmbedding(img_path)
mycol.insert_one({'embedding': embedding, 'img_path': img_path, 'name': 'Tanveer', 'roll no': 'lcs2020021'})
