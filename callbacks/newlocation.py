# -*- coding: utf-8 -*-
"""
Created on Saturday, 2024-06-22 10:43

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
@copyright: Copyright ©  2024 Luca Sung-Min Choi
@license: AGPL v3
@links: https://github.com/lucasmchoi
"""
from dash import Output, Input, State, html
import dash_bootstrap_components as dbc
from pydantic import ValidationError
from constructors.datatypes import LocationModel


def get_newlocation_callbacks(app, db):
    @app.callback(
        Output(
            component_id="data-view",
            component_property="children",
            allow_duplicate=True,
        ),
        Input(component_id="add-locaton-form-submit", component_property="n_clicks"),
        State(component_id="add-location-form-name", component_property="value"),
        State(component_id="add-location-form-street", component_property="value"),
        State(component_id="add-location-form-zip", component_property="value"),
        State(component_id="add-location-form-city", component_property="value"),
        State(component_id="add-location-form-country", component_property="value"),
        State(component_id="add-location-form-room", component_property="value"),
        prevent_initial_call=True,
    )
    def add_location(click, name, street, zipc, city, country, room):

        try:
            location = LocationModel(
                name=name,
                location={
                    "address": {
                        "street": street,
                        "zip": zipc,
                        "city": city,
                        "country": country,
                    },
                    "room": room,
                },
            )
            location_input = location.model_dump(by_alias=True, exclude=["id"])

            inserteddb = db["locations"].insert_one(location_input)

            return (
                dbc.Alert(
                    [
                        "The new location was saved. See ",
                        html.A(
                            "{}".format(location.name),
                            href="/location/{}".format(str(inserteddb.inserted_id)),
                        ),
                    ],
                    color="success",
                ),
            )

        except ValidationError:
            return (
                dbc.Alert("The input was wrong, please try again", color="warning"),
            )
