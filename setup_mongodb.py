# -*- coding: utf-8 -*-
"""
Created on Sunday, 2024-05-05 19:51

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
"""
import os
import secrets
import hashlib
import uuid
import urllib.parse
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING
import gridfs


# add schema validation

uid_salt = os.getenv("USERS_UID_SALT", "horrible salt")
setup_mongodb = bool(os.getenv("MONGO_SETUP", "False"))
setup_example_mongodb = bool(os.getenv("MONGO_SETUP_EXAMPLE", "False"))
mongo_host = os.getenv("MONGO_HOST", "localhost")
mongo_port = os.getenv("MONGO_PORT", "27017")
admin_username = urllib.parse.quote_plus(os.getenv("MONGO_ADMIN_USER", "admin"))
admin_password = urllib.parse.quote_plus(os.getenv("MONGO_ADMIN_PASSWORD", "None"))
hw_username = os.getenv("MONGO_HW_USER", "nfc-hardware-user")
hw_password = os.getenv("MONGO_HW_PASSWORD")
api_username = os.getenv("MONGO_API_USER", "nfc-api-user")
api_password = os.getenv("MONGO_API_PASSWORD")


new_indexes = {
    "users": [
        IndexModel([("name.first", ASCENDING), ("name.last", DESCENDING)], unique=True),
        IndexModel([("userid", ASCENDING)], unique=True),
    ],
    "locations": [],
    "samples": [IndexModel([("sample-number", ASCENDING)], unique=True)],
    "plates": [IndexModel([("plate-number", ASCENDING)], unique=True)],
    "fs.files": [],
    "fs.chunks": [],
}


def create_necessary_indexes(ndb, nindexes):
    existing_cols = ndb.list_collection_names()

    for col in nindexes.keys():
        if col not in existing_cols:
            ndb.create_collection(col)
            if len(nindexes[col]) > 0:
                ndb[col].create_indexes(nindexes[col])

    indexes = []
    for col in ndb.list_collection_names():
        indexes.append(ndb[col].index_information())
    return indexes


if setup_mongodb:
    if hw_password is None:
        hw_password = secrets.token_urlsafe(64)
    if api_password is None:
        api_password = secrets.token_urlsafe(64)

    client = MongoClient(
        f"mongodb://{admin_username}:{admin_password}@{mongo_host}:{mongo_port}/"
    )

    nfc_tracking_db = client["nfc-tracking"]
    gfs = gridfs.GridFS(nfc_tracking_db)

    nfc_tracking_db.command(
        "createUser",
        hw_username,
        pwd=hw_password,
        roles=[
            {"role": "readWrite", "db": "nfc-tracking"},
        ],
    )

    os.environ["MONGO_HW_USER"] = hw_username
    os.environ["MONGO_HW_PASSWORD"] = hw_password

    nfc_tracking_db.command(
        "createUser",
        api_username,
        pwd=api_password,
        roles=[
            {"role": "readWrite", "db": "nfc-tracking"},
        ],
    )

    os.environ["MONGO_API_USER"] = api_username
    os.environ["MONGO_API_PASSWORD"] = api_password

    print(
        f"Mongodb hardware user: {hw_username}\nMongodb hardware password: {hw_password}\n"
    )
    print(f"Mongodb API user: {api_username}\nMongodb API password: {api_password}\n")

    del (
        admin_username,
        admin_password,
        hw_username,
        hw_password,
        api_username,
        api_password,
    )

    create_necessary_indexes(nfc_tracking_db, new_indexes)

    if setup_example_mongodb:
        nfc_example_db = client["nfc-example"]
        create_necessary_indexes(nfc_example_db, new_indexes)

        gfs = gridfs.GridFS(nfc_example_db)

        # random_id on creation of new user to be written onto nfctag
        EXAMPLE_RANDOM_ID = uuid.uuid4().hex
        example_s_userid = EXAMPLE_RANDOM_ID + uid_salt
        example_b_userid = example_s_userid.encode("utf-8")

        EXAMPLE_USERID = None
        EXAMPLE_LOCATIONID = None
        EXAMPLE_SAMPLENUMBER = 1
        EXAMPLE_PLATENUMBER = 1
        EXAMPLE_DOCUMENTID = None
        example_transfertime = datetime.now(tz=timezone.utc)

        EXAMPLE_DOCUMENTID = gfs.put(b"test gfs data")

        EXAMPLE_USERID = (
            nfc_example_db["users"]
            .insert_one(
                {
                    "name": {"first": "Eugene", "last": "Wigner"},
                    "email": "eugene.wigner@physik.tu-berlin.de",
                    "userid": hashlib.sha512(example_b_userid).hexdigest(),
                }
            )
            .inserted_id
        )
        EXAMPLE_LOCATIONID = (
            nfc_example_db["locations"]
            .insert_one(
                {
                    "name": "example laboratory",
                    "location": {
                        "address": {
                            "street": "Hardenbergstraße 36",
                            "zip": "10623",
                            "city": "Berlin",
                            "country": "Germany",
                        },
                        "room": "EW921",
                    },
                }
            )
            .inserted_id
        )

        nfc_example_db["samples"].insert_one(
            {
                "sample-number": EXAMPLE_SAMPLENUMBER,
                "responsible-user": EXAMPLE_USERID,
                "information": {
                    "material": "GaN",
                    "orientation": "0001",
                    "doping": "Mg",
                    "growth": "MOVPE",
                },
                "locations": [
                    {
                        "date": datetime.now(tz=timezone.utc) - timedelta(days=5),
                        "location": EXAMPLE_LOCATIONID,
                        "plate-number": None,
                        "user": EXAMPLE_USERID,
                    },
                    {
                        "date": example_transfertime,
                        "location": EXAMPLE_LOCATIONID,
                        "plate-number": EXAMPLE_PLATENUMBER,
                        "user": EXAMPLE_USERID,
                    },
                ],
                "images": [EXAMPLE_DOCUMENTID],
                "files": [EXAMPLE_DOCUMENTID],
            }
        )
        nfc_example_db["plates"].insert_one(
            {
                "plate-number": EXAMPLE_PLATENUMBER,
                "modifications": [
                    {
                        "date": datetime.now(tz=timezone.utc) - timedelta(days=2),
                        "user": EXAMPLE_USERID,
                        "samples": [],
                    },
                    {
                        "date": example_transfertime,
                        "user": EXAMPLE_USERID,
                        "samples": [EXAMPLE_SAMPLENUMBER],
                    },
                ],
                "locations": [
                    {
                        "date": datetime.now(tz=timezone.utc) - timedelta(days=2),
                        "user": EXAMPLE_USERID,
                        "location": EXAMPLE_LOCATIONID,
                    }
                ],
                "images": [EXAMPLE_DOCUMENTID],
            }
        )

    client.close()
