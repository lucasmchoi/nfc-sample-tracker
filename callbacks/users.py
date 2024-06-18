# -*- coding: utf-8 -*-
"""
Created on Tuesday, 2024-06-18 20:37

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
"""
from dash import dash_table, html
import pandas as pd


def get_users(db):
    projection = {
        "_id": 1,
        "name": {"$concat": ["$name.last", ", ", "$name.first"]},
        "email": 1,
        "userid": 1,
    }
    data = db["users"].find({}, projection)
    ldata = []

    for entry in data:
        pipeline = [
            {"$match": {"responsible-user": entry["_id"]}},
            {"$count": "total_count"},
        ]

        samples_responsibility = list(db["samples"].aggregate(pipeline))[0][
            "total_count"
        ]

        entry["samples"] = "[{}](/users/{})".format(
            samples_responsibility, entry["_id"]
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
                    {"name": "email", "id": "email"},
                    {"name": "samples", "id": "samples", "presentation": "markdown"},
                    {"name": "userid", "id": "userid"},
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
