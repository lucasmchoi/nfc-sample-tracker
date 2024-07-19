# -*- coding: utf-8 -*-
"""
Created on Saturday, 2024-06-22 12:47

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
@copyright: Copyright © 2024 Luca Sung-Min Choi
@license: AGPL v3
@links: https://github.com/lucasmchoi
"""
import os
import hashlib
import uuid
from dash import Output, Input, State, html
import dash_bootstrap_components as dbc
from pydantic import ValidationError
from constructors.models import UserModel


def get_newuser_callbacks(app, db):
    @app.callback(
        Output(
            component_id="data-view",
            component_property="children",
            allow_duplicate=True,
        ),
        Input(component_id="add-user-form-submit", component_property="n_clicks"),
        State(component_id="add-user-form-first-name", component_property="value"),
        State(component_id="add-user-form-last-name", component_property="value"),
        State(component_id="add-user-form-email", component_property="value"),
        prevent_initial_call=True,
    )
    def add_user(click, first, last, email):
        # random_id on creation of new user to be written onto nfctag
        uid_salt = os.getenv("USERS_UID_SALT", "horrible salt")
        new_user_random_id = uuid.uuid4().hex
        string_userid = new_user_random_id + uid_salt
        bytes_userid = string_userid.encode("utf-8")
        hashed_bytes_userid = hashlib.sha512(bytes_userid).hexdigest()

        try:
            user = UserModel(
                name={"first": first, "last": last},
                email=email,
                userid=hashed_bytes_userid,
            )
            user_input = user.model_dump(by_alias=True, exclude=["id"])

            inserteddb = db["users"].insert_one(user_input)
            db["new-users"].insert_one(
                {"user_id": inserteddb.inserted_id, "uuid": new_user_random_id}
            )

            del (
                uid_salt,
                new_user_random_id,
                string_userid,
                bytes_userid,
                hashed_bytes_userid,
            )

            return (
                dbc.Alert(
                    [
                        "The new user was saved. See ",
                        html.A(
                            "{} {}".format(first, last),
                            href="/user/{}".format(str(inserteddb.inserted_id)),
                        ),
                    ],
                    color="success",
                ),
            )

        except ValidationError:
            del (
                uid_salt,
                new_user_random_id,
                string_userid,
                bytes_userid,
                hashed_bytes_userid,
            )

            return (
                dbc.Alert("The input was wrong, please try again", color="warning"),
            )
