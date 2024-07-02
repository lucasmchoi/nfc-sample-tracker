# -*- coding: utf-8 -*-
"""
Created on Sunday, 2024-06-09 08:47

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
@copyright: Copyright © 2024 Luca Sung-Min Choi
@license: AGPL v3
@links: https://github.com/lucasmchoi
"""
from datetime import datetime
from typing import Optional, List, Union
from typing_extensions import Annotated
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class Address(BaseModel):
    """
    Address record for Location in LocationModel
    """

    street: str
    zip: str
    city: str
    country: str


class Location(BaseModel):
    """
    Location record for LocationModel
    """

    address: Address
    room: str


class LocationModel(BaseModel):
    """
    Container for a single location record.
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    location: Location
    creation_date: datetime = Field(alias="creation-date", default=None)
    modification_date: Union[datetime, None] = Field(
        alias="modification-date", default=None
    )
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
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
                "creation-date": datetime(2024, 7, 2, 21, 0, 0),
                "modification-date": None,
            }
        },
    )


class LocationCollection(BaseModel):
    """
    Model for list of LocationModels
    """

    locations: List[LocationModel]


class Name(BaseModel):
    """
    Name record for UserModel
    """

    first: str
    last: str


class UserModel(BaseModel):
    """
    Container for a single user record.
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: Name
    email: EmailStr
    userid: str
    creation_date: datetime = Field(alias="creation-date", default=None)
    modification_date: Union[datetime, None] = Field(
        alias="modification-date", default=None
    )
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": {"first": "Eugene", "last": "Wigner"},
                "email": "eugene.wigner@physik.tu-berlin.de",
                "userid": "d8602a8faec4de4d814c2810b8e331ce5575c3d1cd60f416339d6100c545e694637ec200a4806b1b6487c52eaebb49090bcd077aacefb4387493e35fb62a35bs",
                "creation-date": datetime(2024, 7, 2, 21, 0, 0),
                "modification-date": None,
            }
        },
    )


class UserCollection(BaseModel):
    """
    Model for list of UserModels
    """

    users: List[UserModel]
