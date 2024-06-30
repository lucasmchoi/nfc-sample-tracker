#!/bin/bash

if [ "$HARDWARE" == "True" ]; then
    /.env/bin/python3 -u /nfc-sample-tracker/main_hardware.py &
fi

if [ "$SERVER" == "True" ]; then
    /.env/bin/python3 -u /nfc-sample-tracker/setup_mongodb.py
    /.env/bin/python3 -u /nfc-sample-tracker/main_api.py &
    /.env/bin/python3 -u /nfc-sample-tracker/main_gui.py &
    /.env/bin/python3 -u /nfc-sample-tracker/main_gui_admin.py &
fi
