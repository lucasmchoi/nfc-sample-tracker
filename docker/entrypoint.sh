#!/bin/bash

if [ "$HARDWARE" == "True" ]; then
    /.venv/bin/python3 -u /nfc-sample-tracker/main_hardware.py &
    
fi

if [ "$SERVER" == "True" ]; then
    /.venv/bin/python3 -u /nfc-sample-tracker/setup_mongodb.py
    if [ "$STOP_API" != "True" ]; then
        uvicorn main_api:app --host 0.0.0.0 --port 8081 --workers 4 &
    fi
    if [ "$STOP_GUI_MAIN" != "True" ]; then
        if [ "$GUI_DEBUG" == "True" ]; then
            /.venv/bin/python3 -u /nfc-sample-tracker/main_gui.py &
        else
            gunicorn main_gui_admin:server -b 0.0.0.0:8082 --workers 4 &
    fi
    fi
    if [ "$STOP_GUI_ADMIN" != "True" ]; then
        if [ "$GUI_DEBUG" == "True" ]; then
            /.venv/bin/python3 -u /nfc-sample-tracker/main_gui_admin.py &
        else
            gunicorn main_gui_admin:server -b 0.0.0.0:8083 --workers 4 &
    fi
fi

wait
