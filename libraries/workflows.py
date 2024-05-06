# -*- coding: utf-8 -*-
"""
Created on Monday, 2024-05-06 13:28

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
"""
import uuid
import os
import hashlib
from typing import Type
from datetime import datetime, timezone
from pirc522 import RFID
from pymongo import MongoClient, DESCENDING
import ndef
from libraries.nfcreader import (
    begin_tag,
    stop_tag,
    check_ntag_usermemeory_beginning,
    create_ndef_message,
    write_ntag_message,
    read_ntag_container,
    find_and_parse_ndef_message,
)

# from libraries.camera import capture_image


mongo_host = os.getenv("MONGO_HOST", "localhost")
mongo_port = os.getenv("MONGO_PORT", "27017")
hw_username = os.getenv("MONGO_HW_USER", "nfc-hardware-user")
hw_password = os.getenv("MONGO_HW_PASSWORD")
uid_salt = os.getenv("USERS_UID_SALT", "horrible salt")
userurl = os.getenv("USERS_PROFILE_URL", "example.com/user")
sampleurl = os.getenv("SAMPLES_OVERVIEW_URL", "example.com/sample")


def register_new_user(reader: Type[RFID]) -> bool:
    """callback function to register new uuid for user and
    write corresponding ntag with link to USERS_PROFILE_URL

    Args:
        reader (Type[RFID]): RFID class from pirc522

    Returns:
        bool: bool to indicate error
    """
    new_user_uuid = uuid.uuid4().hex
    s_userid = new_user_uuid + uid_salt
    userid = hashlib.sha512(s_userid.encode("utf-8")).hexdigest()

    error_b, _ = begin_tag(reader)
    if not error_b:
        error_c, empty = check_ntag_usermemeory_beginning(reader)
        error_cw = not empty
        if not error_c and empty:
            client = MongoClient(
                f"mongodb://{hw_username}:{hw_password}@{mongo_host}:{mongo_port}/"
            )

            nfc_tracking_db = client["nfc-tracking"]

            r0 = ndef.TextRecord("USER")
            r1 = ndef.UriRecord(f"https://{userurl}/{new_user_uuid}")
            r2 = ndef.TextRecord(f"{new_user_uuid}")
            message = [r0, r1, r2]
            msg = create_ndef_message(message)
            error_w = write_ntag_message(reader, msg, 4)

            nfc_tracking_db["users"].insert_one(
                {
                    "userid": userid,
                }
            )

            client.close()

    error_s = stop_tag(reader)

    return any(error_b, error_c, error_cw, error_s, error_w)


def register_new_sample(reader: Type[RFID]) -> bool:
    current_tag = None
    client = MongoClient(
        f"mongodb://{hw_username}:{hw_password}@{mongo_host}:{mongo_port}/"
    )

    nfc_tracking_db = client["nfc-tracking"]

    # capture image

    errors = []

    # TODO capture image and store to data + add uid to sample entry
    # time.sleep(1)
    # try:
    #     picam2_image, bytes_image = capture_image()
    # except:
    #     errors.append(True)

    reader.wait_for_tag(5)
    error, uid = begin_tag(reader)
    current_tag = uid
    errors.append(error)
    error, data = read_ntag_container(reader, "user memory")
    errors.append(error)
    errors.append(stop_tag(reader))
    if not error:
        error, _, ndef_messages = find_and_parse_ndef_message(data)
        errors.append(error)
        if not error:
            error = ndef_messages[0][0] != "USER"
            errors.append(error)
            if not error:
                user_uuid = ndef_messages[0][2]

                new_sample_number = 1

                if nfc_tracking_db["samples"].count_documents({}) > 0:
                    new_sample_number += (
                        nfc_tracking_db["samples"]
                        .find({}, {"_id": 0, "sample-number": 1})
                        .sort("sample-number", DESCENDING)
                        .limit(1)[0]["sample-number"]
                    )

                r0 = ndef.TextRecord("SAMPLE")
                r1 = ndef.UriRecord(
                    f"https://{sampleurl}/{new_sample_number}"
                )
                r2 = ndef.TextRecord(f"{new_sample_number}")
                r3 = ndef.TextRecord(f"{user_uuid}")
                message = [r0, r1, r2, r3]
                msg = create_ndef_message(message)

                for i in range(2):
                    reader.wait_for_tag(5)
                    while current_tag == uid and not error:
                        error, uid = begin_tag(reader)
                    errors.append(error)

                    error_c, empty = check_ntag_usermemeory_beginning(reader)
                    error_cw = not empty
                    errors.append(error_c)
                    errors.append(error_cw)
                    errors.append(stop_tag(reader))

                    if not error_c and error_cw:
                        error = write_ntag_message(reader, msg, 4)

                if not error:
                    nfc_tracking_db["samples"].insert_one(
                        {
                            "sample-number": new_sample_number,
                            "responsible-user": user_uuid,
                            "locations": [
                                {
                                    "date": datetime.now(tz=timezone.utc),
                                    # "location": default_location,
                                    "plate-number": None,
                                    "user": user_uuid,
                                }
                            ],
                            # "images": [example_documentid],
                            # "files": [example_documentid],
                        }
                    )
                # write new sample to database
    client.close()

    return any(errors)
