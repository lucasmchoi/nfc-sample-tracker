# -*- coding: utf-8 -*-
"""
Created on Tuesday, 2024-06-18 21:08

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
"""
from dash import dash_table, html
import pandas as pd


def get_locations(db):
    projection = {
        "_id": 1,
        "name": 1,
        "room": "$location.room",
        "address": {
            "$concat": [
                "$location.address.street",
                ", ",
                "$location.address.zip",
                " ",
                "$location.address.city",
                ", ",
                "$location.address.country",
            ]
        },
    }

    data = db["locations"].find({}, projection)
    ldata = []
    for entry in data:
        pipeline = [
            {
                "$project": {
                    "sample-number": 1,
                    "current_location": {
                        "$arrayElemAt": [
                            {
                                "$slice": [
                                    {
                                        "$sortArray": {
                                            "input": "$locations",
                                            "sortBy": {"date": -1},
                                        }
                                    },
                                    1,
                                ]
                            },
                            0,
                        ]
                    },
                }
            },
            {"$match": {"current_location.location": entry["_id"]}},
            {"$count": "total_count"},
        ]

        samples_at_location_list = list(db["samples"].aggregate(pipeline))

        if len(samples_at_location_list) > 0:
            samples_at_location_list = samples_at_location_list[0]
            if "total_count" not in samples_at_location_list:
                samples_at_location = 0
            else:
                samples_at_location = samples_at_location_list.get("total_count")
        else:
            samples_at_location = 0

        entry["samples at location"] = "[{}](/location/{})".format(
            samples_at_location, entry["_id"]
        )
        entry["_id"] = str(entry["_id"])
        ldata.append(entry)
    df = pd.DataFrame(ldata)

    return html.Div(
        [
            html.Div([html.H2("Locations")]),
            html.Div(
                [
                    dash_table.DataTable(
                        data=df.to_dict("records"),
                        columns=[
                            {
                                "name": "name",
                                "id": "name",
                                "presentation": "markdown",
                            },
                            {
                                "name": "room",
                                "id": "room",
                                "presentation": "markdown",
                            },
                            {
                                "name": "address",
                                "id": "address",
                                "presentation": "markdown",
                            },
                            {
                                "name": "samples at location",
                                "id": "samples at location",
                                "presentation": "markdown",
                            },
                            {"name": "_id", "id": "_id", "presentation": "markdown"},
                        ],
                        style_cell={
                            "whiteSpace": "normal",
                            "height": "auto",
                            "maxWidth": 0,
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "textAlign": "center",
                        },
                        css=[dict(selector="p", rule="margin: 0; text-align: center")],
                        markdown_options={"link_target": "_self"},
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                    ),
                ]
            ),
        ]
    )
