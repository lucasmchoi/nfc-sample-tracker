# -*- coding: utf-8 -*-
"""
Created on Friday, 2024-05-03 19:29

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
"""
from libraries.workflows import *
from pirc522 import RFID
from RPi import GPIO
import os


import socket
import urllib.request
global button_interaction
button_interaction = {}


def set_button_interaction(channel):
    global button_interaction
    button_interaction[str(channel)] = True
    pass


# picam2_image, bytes_image = capture_image()

rdr_bus = os.getenv('MFRC522_BUS', 0)
rdr_device = os.getenv('MFRC522_DEVICE', 0)
rdr_speed = os.getenv('MFRC522_SPEED', 1000000)
rdr_pin_rst = os.getenv('MFRC522_PIN_RST', 22)
rdr_pin_ce = os.getenv('MFRC522_PIN_CE', 0)
rdr_pin_rst = os.getenv('MFRC522_PIN_IRQ', 18)
rdr_antenna_gain = os.getenv('MFRC522_ANTENNA_GAIN', None)

btn_pin_new_user =  os.getenv('BUTTON_PIN_NEW_USER', 10)
btn_pin_new_sample =  os.getenv('BUTTON_PIN_NEW_USER', 11)

button_interaction[str(btn_pin_new_user)] = False
button_interaction[str(btn_pin_new_sample)] = False


rdr = RFID(bus=rdr_bus, device=rdr_device, speed=rdr_speed, pin_rst=rdr_pin_rst, pin_ce=rdr_pin_ce, pin_irq=rdr_pin_rst, antenna_gain=rdr_antenna_gain)


GPIO.setmode(GPIO.BOARD)

GPIO.setup(btn_pin_new_user, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(btn_pin_new_user, GPIO.RISING, callback=set_button_interaction, bouncetime=200)

GPIO.setup(btn_pin_new_sample, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(btn_pin_new_sample, GPIO.RISING, callback=set_button_interaction, bouncetime=200)


while True:
    errors = []
    if button_interaction[str(btn_pin_new_user)]:
        errors.append(register_new_user(rdr))
    elif button_interaction[str(btn_pin_new_sample)]:
        errors.append(register_new_sample(rdr))
    else:
        error, uid = begin_tag(rdr)
        errors.append(error)
        # return sample information + location
        errors.append(stop_tag(rdr))


    # try:
    #     urllib.request.urlopen("https://hc-ping.com/your-uuid-here", timeout=10)
    # except socket.error as e:
    #     # Log ping failure here...
    #     print("Ping failed: %s" % e)