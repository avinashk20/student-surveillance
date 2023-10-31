#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 23:39:02 2023

@author: avinash
"""

import telegram

bot = telegram.Bot(token='6136575757:AAHgPS3th1FATZpPCFMD_Ajr0voHdJqATIE')
chat_id = '-1001891865107'


async def sendAlert(caption, image_path, cam_img):
    with open(image_path, 'rb') as f:
        await bot.send_photo(chat_id=chat_id, photo=f, caption=caption)
        await bot.send_photo(chat_id=chat_id, photo=cam_img, caption='cam image')
    

