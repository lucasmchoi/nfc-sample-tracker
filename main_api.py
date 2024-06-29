# -*- coding: utf-8 -*-
"""
Created on Saturday, 2024-06-08 22:04

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
@copyright: Copyright ©  2024 Luca Sung-Min Choi
@license: AGPL v3
@links: https://github.com/lucasmchoi
"""
import os
from fastapi import FastAPI, HTTPException
from bson import ObjectId
import motor.motor_asyncio
from constructors.datatypes import (
    LocationModel,
    UserModel,
    LocationCollection,
    UserCollection,
)


uid_salt = os.getenv("USERS_UID_SALT", "horrible salt")
mongo_host = os.getenv("MONGO_HOST", "localhost")
mongo_port = os.getenv("MONGO_PORT", "27017")
api_username = os.getenv("MONGO_API_USER", "nfc-api-user")
api_password = os.getenv("MONGO_API_PASSWORD")


client = motor.motor_asyncio.AsyncIOMotorClient(
    # f"mongodb://{api_username}:{api_password}@{mongo_host}:{mongo_port}/"
    f"mongodb://admin:admin@{mongo_host}:{mongo_port}/"
)
db = client["nfc-example"]  # ["nfc-tracking"]
locations_collection = db["locations"]
users_collection = db["users"]


app = FastAPI()


@app.get(
    "/locations/",
    response_description="Get list of all locations",
    response_model=LocationCollection,
    response_model_by_alias=False,
)
async def show_all_locations():
    """
    Get all location records
    """

    return LocationCollection(locations=await locations_collection.find().to_list(1000))


@app.get(
    "/locations/{uid}",
    response_description="Get a single location",
    response_model=LocationModel,
    response_model_by_alias=False,
)
async def show_location(uid: str):
    """
    Get the record for a specific location, looked up by `id`.
    """

    if (
        location := await locations_collection.find_one({"_id": ObjectId(uid)})
    ) is not None:
        return location

    raise HTTPException(status_code=404, detail=f"Location {uid} not found")


@app.get(
    "/users/",
    response_description="Get list of all users",
    response_model=UserCollection,
    response_model_by_alias=False,
)
async def show_all_users():
    """
    Get all user records
    """

    return UserCollection(users=await users_collection.find().to_list(1000))


@app.get(
    "/users/{uid}",
    response_description="Get a single user",
    response_model=UserModel,
    response_model_by_alias=False,
)
async def show_user(uid: str):
    """
    Get the record for a specific user, looked up by `id`.
    """

    if (user := await users_collection.find_one({"userid": uid})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {uid} not found")
