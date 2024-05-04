# -*- coding: utf-8 -*-
"""
Created on Saturday, 2024-05-04 12:53

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
"""
from picamera2 import Picamera2
import time
import io


def capture_image():
    bytes_image = io.BytesIO()

    picam2 = Picamera2()

    picam2.start()
    time.sleep(1)

    picam2_image = picam2.capture_image()

    picam2.close()

    picam2_image.save(bytes_image, format='JPEG')

    return picam2_image, bytes_image