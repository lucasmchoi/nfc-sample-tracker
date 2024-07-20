# -*- coding: utf-8 -*-
"""
Created on Friday, 2024-07-19 22:47

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
@copyright: Copyright © 2024 Luca Sung-Min Choi
@license: AGPL v3
@links: https://github.com/lucasmchoi
"""

import os
import urllib.parse
from datetime import datetime
from typing import Optional, List, Union
from typing_extensions import Annotated
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from constructors.helpers import get_current_date


class Environment(BaseModel):
    """
    Environment variables
    """

    mongo_host: str = Field(default=os.getenv("MONGO_HOST", "localhost"))
    mongo_port: int = Field(default=os.getenv("MONGO_PORT", "27017"))
    mongo_db: str = Field(default=os.getenv("MONGO_DATABASE", "nfc-tracking"))

    admin_user: str = Field(
        default=urllib.parse.quote_plus(os.getenv("MONGO_ADMIN_USER", "admin"))
    )
    admin_pass: str = Field(
        default=urllib.parse.quote_plus(os.getenv("MONGO_ADMIN_PASSWORD", "None"))
    )

    mongo_setup: bool = Field(default=os.getenv("MONGO_SETUP", "False"))
    mongo_setup_example: bool = Field(default=os.getenv("MONGO_SETUP_EXAMPLE", "False"))

    gui_user: str = Field(default=os.getenv("MONGO_GUI_USER", "nfc-gui-user"))
    gui_pass: str = Field(default=os.getenv("MONGO_GUI_PASSWORD"))
    gui_port: int = Field(default=os.getenv("GUI_ADMIN_PORT", "8082"))
    gui_debug: bool = Field(default=os.getenv("GUI_DEBUG", "False"))
    gui_admin_port: int = Field(default=os.getenv("GUI_ADMIN_PORT", "8083"))

    api_user: str = Field(default=os.getenv("MONGO_API_USER", "nfc-api-user"))
    api_pass: str = Field(default=os.getenv("MONGO_API_PASSWORD"))

    hw_user: str = Field(default=os.getenv("MONGO_HW_USER", "nfc-hardware-user"))
    hw_pass: str = Field(default=os.getenv("MONGO_HW_PASSWORD"))

    uid_salt: str = Field(default=os.getenv("USERS_UID_SALT", "horrible salt"))


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
    creation_date: datetime = Field(alias="creation-date", default=get_current_date())
    modification_date: Union[datetime, None] = Field(
        alias="modification-date", default=get_current_date()
    )
    model_config = ConfigDict(
        populate_by_name=True,
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
    creation_date: datetime = Field(alias="creation-date", default=get_current_date())
    modification_date: Union[datetime, None] = Field(
        alias="modification-date", default=get_current_date()
    )
    model_config = ConfigDict(
        populate_by_name=True,
    )


class UserCollection(BaseModel):
    """
    Model for list of UserModels
    """

    users: List[UserModel]


class PlateLocation(BaseModel):
    """
    Container for a single plate location record
    """

    date: datetime = Field(default=get_current_date())
    user: PyObjectId
    location: PyObjectId


class PlateModification(BaseModel):
    """
    Container for a single plate modification record
    """

    date: datetime = Field(default=get_current_date())
    user: PyObjectId
    samples: List[int]


class PlateModel(BaseModel):
    """
    Container for a single plate record
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    plate_number: int = Field(alias="plate-number", default=None)
    modifications: List[PlateModification] = Field(default=[])
    locations: List[PlateLocation] = Field(default=[])
    images: List[PyObjectId] = Field(default=[])
    creation_date: datetime = Field(alias="creation-date", default=get_current_date())
    model_config = ConfigDict(
        populate_by_name=True,
    )


class PlateCollection(BaseModel):
    """
    Model for list of PlateModels
    """

    plates: List[PlateModel]


class SampleLocation(BaseModel):
    """
    Container for a single sample location record
    """

    date: datetime = Field(default=get_current_date())
    location: PyObjectId
    plate_number: PyObjectId = Field(alias="plate-number")
    user: PyObjectId
    model_config = ConfigDict(
        populate_by_name=True,
    )


class SampleLost(BaseModel):
    """
    Container for a single sample lost record
    """

    date: Union[datetime, None] = Field(default=get_current_date())
    note: Union[str, None]


class SampleDamage(BaseModel):
    """
    Container for a single sample damage record
    """

    date: Union[datetime, None] = Field(default=get_current_date())
    note: Union[str, None]


class SampleInformationModel(BaseModel):
    """
    Container for a single sample information record
    """

    origin: PyObjectId
    material: str
    orientation: str
    doping: str
    growth: str
    note: Union[str, None] = Field(default=None)
    damaged: SampleDamage = Field(default=SampleDamage(date=None, note=None))
    lost: SampleLost = Field(default=SampleLost(date=None, note=None))


class OwnerModel(BaseModel):
    """
    Container for a single owner record
    """

    date: datetime = Field(default=get_current_date())
    user: PyObjectId


class SampleModel(BaseModel):
    """
    Container for a single sample record
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    sample_number: int = Field(alias="sample-number", default=None)
    owners: List[OwnerModel]
    information: SampleInformationModel
    locations: List[SampleLocation] = Field(default=[])
    images: List[PyObjectId] = Field(default=[])
    files: List[PyObjectId] = Field(default=[])
    creation_date: datetime = Field(alias="creation-date", default=get_current_date())
    model_config = ConfigDict(
        populate_by_name=True,
    )


class SampleCollection(BaseModel):
    """
    Model for list of SampleModels
    """

    samples: List[SampleModel]


class NewPlate(BaseModel):
    """
    Container for a single new-plates record
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    plate_id: PyObjectId
    plate_number: int = Field(alias="plate-number", default=None)
    creation_date: datetime = Field(alias="creation-date", default=get_current_date())
    model_config = ConfigDict(
        populate_by_name=True,
    )


class NewUser(BaseModel):
    """
    Container for a single new-users record
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    uuid: str
    creation_date: datetime = Field(alias="creation-date", default=get_current_date())
    model_config = ConfigDict(
        populate_by_name=True,
    )


class NewSample(BaseModel):
    """
    Container for a single new-samples record
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    sample_id: PyObjectId
    sample_number: int = Field(alias="sample-number", default=None)
    material: str
    orientation: str
    origin: str
    creation_date: datetime = Field(alias="creation-date", default=get_current_date())
    model_config = ConfigDict(
        populate_by_name=True,
    )
