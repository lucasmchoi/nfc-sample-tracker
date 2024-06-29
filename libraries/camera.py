# -*- coding: utf-8 -*-
"""
Created on Saturday, 2024-05-04 12:53

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
@copyright: Copyright © 2024 Luca Sung-Min Choi
@license: AGPL v3
@links: https://github.com/lucasmchoi
"""
import time
from io import BytesIO
from typing import Type
from PIL import Image
from picamera2 import Picamera2


def capture_image() -> tuple[Type[Image], Type[BytesIO]]:
    """capture image using picamera2 and return Pillow image and bytes

    Returns:
        _type_: _description_
    """
    bytes_image = BytesIO()

    picam2 = Picamera2()

    picam2.start()
    time.sleep(1)

    picam2_image = picam2.capture_image()

    picam2.close()

    picam2_image.save(bytes_image, format='JPEG')

    return picam2_image, bytes_image
