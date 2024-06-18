# -*- coding: utf-8 -*-
"""
Created on Tuesday, 2024-06-18 22:22

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
"""
from dash import dash_table, html
import pandas as pd
from bson.objectid import ObjectId


def get_user(db, oid):

    projection = {
        "_id": 0,
        "name": {"$concat": ["$name.first", " ", "$name.last"]},
    }
    responsible_person = db["users"].find_one({"_id": ObjectId(oid)}, projection)[
        "name"
    ]

    pipeline = [
        {"$match": {"responsible-user": ObjectId(oid)}},
        {
            "$project": {
                "_id": 0,
                "sample-number": 1,
                "material": "$information.material",
                "orientation": "$information.orientation",
                "doping": "$information.doping",
                "growth": "$information.growth",
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
        {
            "$project": {
                "sample-number": 1,
                "material": 1,
                "orientation": 1,
                "doping": 1,
                "growth": 1,
                "current_location": "$current_location.location",
            }
        },
    ]

    samples = list(db["samples"].aggregate(pipeline))

    for entry in samples:
        locationname = db["locations"].aggregate(
            [
                {"$match": {"_id": entry["current_location"]}},
                {"$project": {"_id": 0, "name": 1}},
            ]
        )
        entry["current_location"] = list(locationname)[0]["name"]

    df = pd.DataFrame(samples)

    return html.Div(
        [
            html.Div([html.H2(f"{responsible_person}'s samples")]),
            html.Div(
                [
                    dash_table.DataTable(
                        data=df.to_dict("records"),
                        columns=[
                            {"name": "sample number", "id": "sample-number"},
                            {
                                "name": "current location",
                                "id": "current_location",
                                "presentation": "markdown",
                            },
                            {"name": "material", "id": "material"},
                            {"name": "orientation", "id": "orientation"},
                            {"name": "doping", "id": "doping"},
                            {"name": "growth", "id": "growth"},
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
            ),
        ]
    )
