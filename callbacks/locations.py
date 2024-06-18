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
                "\n",
                "$location.address.zip",
                "\n",
                "$location.address.city",
                "\n",
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

        samples_at_location = list(db["samples"].aggregate(pipeline))[0]["total_count"]

        entry["samples at location"] = "[{}](/locations/{})".format(
            samples_at_location, entry["_id"]
        )
        entry.pop("_id", None)
        ldata.append(entry)
    df = pd.DataFrame(ldata)

    return html.Div(
        [
            dash_table.DataTable(
                data=df.to_dict("records"),
                columns=[
                    {"name": "name", "id": "name"},
                    {"name": "room", "id": "room"},
                    {"name": "address", "id": "address"},
                    {
                        "name": "samples at location",
                        "id": "samples at location",
                        "presentation": "markdown",
                    },
                ],
                style_cell={
                    "whiteSpace": "pre-line",
                    "height": "auto",
                    "maxWidth": 0,
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                },
            ),
        ]
    )
