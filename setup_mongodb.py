# -*- coding: utf-8 -*-
"""
Created on Sunday, 2024-05-05 19:51

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
"""
from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING
import urllib.parse
import hashlib
import uuid
import gridfs
import os
import secrets
from datetime import datetime, timezone, timedelta


# TODO add schema validation

uid_salt = os.getenv("USERS_UID_SALT", "horrible salt")
setup_mongodb = bool(os.getenv("MONGO_SETUP", False))
setup_example_mongodb = bool(os.getenv("MONGO_SETUP_EXAMPLE", False))
mongo_host = os.getenv("MONGO_HOST", "localhost")
mongo_port = os.getenv("MONGO_PORT", 27017)
admin_username = urllib.parse.quote_plus(os.getenv("MONGO_ADMIN_USER", "admin"))
admin_password = urllib.parse.quote_plus(os.getenv("MONGO_ADMIN_PASSWORD", "None"))
hw_username = os.getenv("MONGO_HW_USER", "nfc-hardware-user")
hw_password = os.getenv("MONGO_HW_PASSWORD", None)
api_username = os.getenv("MONGO_API_USER", "nfc-api-user")
api_password = os.getenv("MONGO_API_PASSWORD", None)


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
    if hw_password == None:
        hw_password = secrets.token_urlsafe(64)
    if api_password == None:
        api_password = secrets.token_urlsafe(64)

    client = MongoClient(
        "mongodb://%s:%s@%s:%s/"
        % (admin_username, admin_password, mongo_host, mongo_port)
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
        "Mongodb hardware user: {}\nMongodb hardware password: {}\n".format(
            hw_username, hw_password
        )
    )
    print(
        "Mongodb API user: {}\nMongodb API password: {}\n".format(
            api_username, api_password
        )
    )

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
        example_random_id = uuid.uuid4().hex
        example_s_userid = example_random_id + uid_salt
        example_b_userid = example_s_userid.encode("utf-8")

        example_userid = None
        example_locationid = None
        example_samplenumber = 1
        example_platenumber = 1
        example_documentid = None
        example_transfertime = datetime.now(tz=timezone.utc)

        example_documentid = gfs.put(b"test gfs data")

        example_userid = (
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
        example_locationid = (
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
                "sample-number": example_samplenumber,
                "responsible-user": example_userid,
                "information": {
                    "material": "GaN",
                    "orientation": "0001",
                    "doping": "Mg",
                    "growth": "MOVPE",
                },
                "locations": [
                    {
                        "date": datetime.now(tz=timezone.utc) - timedelta(days=5),
                        "location": example_locationid,
                        "plate-number": None,
                        "user": example_userid,
                    },
                    {
                        "date": example_transfertime,
                        "location": example_locationid,
                        "plate-number": example_platenumber,
                        "user": example_userid,
                    },
                ],
                "images": [example_documentid],
                "files": [example_documentid],
            }
        )
        nfc_example_db["plates"].insert_one(
            {
                "plate-number": example_platenumber,
                "modifications": [
                    {
                        "date": datetime.now(tz=timezone.utc) - timedelta(days=2),
                        "user": example_userid,
                        "samples": [],
                    },
                    {
                        "date": example_transfertime,
                        "user": example_userid,
                        "samples": [example_samplenumber],
                    },
                ],
                "locations": [
                    {
                        "date": datetime.now(tz=timezone.utc) - timedelta(days=2),
                        "user": example_userid,
                        "location": example_locationid,
                    }
                ],
                "images": [example_documentid],
            }
        )
