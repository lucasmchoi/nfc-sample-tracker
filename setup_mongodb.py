# -*- coding: utf-8 -*-
"""
Created on Sunday, 2024-05-05 19:51

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
@copyright: Copyright © 2024 Luca Sung-Min Choi
@license: AGPL v3
@links: https://github.com/lucasmchoi
"""
import os
import secrets
import hashlib
import uuid
import urllib.parse
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING
import gridfs


SETUPFILE = "/mongodbissetup"

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
gui_username = os.getenv("MONGO_GUI_USER", "nfc-gui-user")
gui_password = os.getenv("MONGO_GUI_PASSWORD")

users_passwords_env = [
    ["MONGO_HW_USER", "MONGO_HW_PASSWORD"],
    ["MONGO_API_USER", "MONGO_API_PASSWORD"],
    ["MONGO_GUI_USER", "MONGO_GUI_PASSWORD"],
]

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
    "new-users": [],
    "new-samples": [],
    "new-plates": [],
}


def create_necessary_indexes(ndb, nindexes):
    """Function to create new indexes in a database

    Args:
        ndb (MongoDB database): MongoDB database of pymongo
        nindexes (dict): Dictionary of new index and properties, see new_indexes

    Returns:
        list: return index informations of existing indexes after creating new ones
    """
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


if setup_mongodb and os.path.isfile(SETUPFILE):
    if hw_password is None:
        hw_password = secrets.token_urlsafe(64)
    if api_password is None:
        api_password = secrets.token_urlsafe(64)
    if gui_password is None:
        gui_password = secrets.token_urlsafe(64)

    users_passwords = [
        [hw_username, hw_username, "MONGO_HW_USER", "MONGO_HW_PASSWORD"],
        [api_username, api_password, "MONGO_API_USER", "MONGO_API_PASSWORD"],
        [gui_username, gui_username, "MONGO_GUI_USER", "MONGO_GUI_PASSWORD"],
    ]

    client = MongoClient(
        f"mongodb://{admin_username}:{admin_password}@{mongo_host}:{mongo_port}/"
    )

    nfc_tracking_db = client["nfc-tracking"]
    gfs = gridfs.GridFS(nfc_tracking_db)

    for u_pw in users_passwords:
        nfc_tracking_db.command(
            "createUser",
            u_pw[0],
            u_pw[1],
            roles=[
                {"role": "readWrite", "db": "nfc-tracking"},
            ],
        )

        os.environ[u_pw[2]] = u_pw[0]
        os.environ[u_pw[3]] = u_pw[1]

    print(
        f"Mongodb hardware user: {hw_username}\nMongodb hardware password: {hw_password}\n"
    )
    print(f"Mongodb API user: {api_username}\nMongodb API password: {api_password}\n")
    print(f"Mongodb GUI user: {gui_username}\nMongodb GUI password: {gui_password}\n")

    del (
        users_passwords,
        admin_username,
        admin_password,
        hw_username,
        hw_password,
        api_username,
        api_password,
        gui_username,
        gui_password,
    )

    create_necessary_indexes(nfc_tracking_db, new_indexes)

    if setup_example_mongodb:
        nfc_example_db = client["nfc-example"]
        create_necessary_indexes(nfc_example_db, new_indexes)

        for u_pw_env in users_passwords_env:
            nfc_example_db.command(
                "createUser",
                os.environ[u_pw_env[0]],
                pwd=os.environ[u_pw_env[1]],
                roles=[
                    {"role": "readWrite", "db": "nfc-example"},
                ],
            )

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
        EXAMPLE_TIME = datetime.now(tz=timezone.utc)

        EXAMPLE_DOCUMENTID = gfs.put(b"test gfs data")

        EXAMPLE_USERID = (
            nfc_example_db["users"]
            .insert_one(
                {
                    "name": {"first": "Eugene", "last": "Wigner"},
                    "email": "eugene.wigner@physik.tu-berlin.de",
                    "userid": hashlib.sha512(example_b_userid).hexdigest(),
                    "creation-date": EXAMPLE_TIME - timedelta(weeks=10),
                    "modification-date": None,
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
                    "creation-date": EXAMPLE_TIME - timedelta(weeks=10),
                    "modification-date": EXAMPLE_TIME,
                }
            )
            .inserted_id
        )

        EXAMPLE_SAMPLEID = nfc_example_db["samples"].insert_one(
            {
                "sample-number": EXAMPLE_SAMPLENUMBER,
                "owners": [{"date": EXAMPLE_TIME, "user": EXAMPLE_USERID}],
                "information": {
                    "origin": EXAMPLE_LOCATIONID,
                    "material": "GaN",
                    "orientation": "0001",
                    "doping": "Mg",
                    "growth": "MOVPE",
                    "note": "No notes",
                    "damaged": {
                        "date": EXAMPLE_TIME - timedelta(days=1),
                        "note": "broken while cleaning",
                    },
                    "lost": {
                        "date": EXAMPLE_TIME - timedelta(hours=1),
                        "note": "lost behind the couch",
                    },
                },
                "locations": [
                    {
                        "date": EXAMPLE_TIME - timedelta(days=5),
                        "location": EXAMPLE_LOCATIONID,
                        "plate-number": None,
                        "user": EXAMPLE_USERID,
                    },
                    {
                        "date": EXAMPLE_TIME,
                        "location": EXAMPLE_LOCATIONID,
                        "plate-number": EXAMPLE_PLATENUMBER,
                        "user": EXAMPLE_USERID,
                    },
                ],
                "images": [EXAMPLE_DOCUMENTID],
                "files": [EXAMPLE_DOCUMENTID],
                "creation-date": EXAMPLE_TIME - timedelta(weeks=5),
            }
        )

        EXAMPLE_PLATEID = nfc_example_db["plates"].insert_one(
            {
                "plate-number": EXAMPLE_PLATENUMBER,
                "modifications": [
                    {
                        "date": EXAMPLE_TIME - timedelta(days=2),
                        "user": EXAMPLE_USERID,
                        "samples": [],
                    },
                    {
                        "date": EXAMPLE_TIME,
                        "user": EXAMPLE_USERID,
                        "samples": [EXAMPLE_SAMPLENUMBER],
                    },
                ],
                "locations": [
                    {
                        "date": EXAMPLE_TIME - timedelta(days=2),
                        "user": EXAMPLE_USERID,
                        "location": EXAMPLE_LOCATIONID,
                    }
                ],
                "images": [EXAMPLE_DOCUMENTID],
                "creation-date": EXAMPLE_TIME - timedelta(days=2),
            }
        )

        nfc_example_db["new-users"].insert_one(
            {
                "user_id": EXAMPLE_USERID,
                "uuid": EXAMPLE_RANDOM_ID,
                "creation-date": EXAMPLE_TIME - timedelta(weeks=10),
            }
        )

        nfc_example_db["new-samples"].insert_one(
            {
                "sample_id": EXAMPLE_SAMPLEID,
                "sample-number": EXAMPLE_SAMPLENUMBER,
                "material": "GaN",
                "orientation": "0001",
                "origin": "example laboratory",
                "creation-date": EXAMPLE_TIME - timedelta(weeks=5),
            }
        )

        nfc_example_db["new-plates"].insert_one(
            {
                "plate_id": EXAMPLE_PLATEID,
                "plate-number": EXAMPLE_PLATENUMBER,
                "creation-date": EXAMPLE_TIME - timedelta(days=2),
            }
        )

    with open(SETUPFILE, "w", encoding="utf-8") as empty_file:
        pass

    client.close()
