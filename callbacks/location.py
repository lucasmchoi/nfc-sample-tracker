# -*- coding: utf-8 -*-
"""
Created on Tuesday, 2024-06-18 23:16

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
"""
from dash import dash_table, html
import pandas as pd
from bson.objectid import ObjectId


def get_location(db, oid):

    projection = {
        "_id": 0,
        "name": 1,
    }
    selected_location = db["locations"].find_one({"_id": ObjectId(oid)}, projection)[
        "name"
    ]

    pipeline = [
        {
            "$project": {
                "_id": 0,
                "sample-number": 1,
                "material": "$information.material",
                "orientation": "$information.orientation",
                "doping": "$information.doping",
                "growth": "$information.growth",
                "responsible-user": 1,
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
                "responsible-user": 1,
            }
        },
        {"$match": {"current_location": ObjectId(oid)}},
        {
            "$project": {
                "sample-number": 1,
                "material": 1,
                "orientation": 1,
                "doping": 1,
                "growth": 1,
                "responsible-user": 1,
            }
        },
    ]

    samples = list(db["samples"].aggregate(pipeline))

    for entry in samples:
        projection = {
            "_id": 1,
            "name": {"$concat": ["$name.first", " ", "$name.last"]},
        }

        responsible_user = db["users"].find_one(
            {"_id": entry["responsible-user"]}, projection
        )

        entry["responsible-user"] = "[{}](/user/{})".format(
            responsible_user["name"], responsible_user["_id"]
        )

    df = pd.DataFrame(samples)

    return html.Div(
        [
            html.Div([html.H2(f"samples at location: {selected_location}")]),
            html.Div(
                [
                    dash_table.DataTable(
                        data=df.to_dict("records"),
                        columns=[
                            {
                                "name": "sample number",
                                "id": "sample-number",
                                "presentation": "markdown",
                            },
                            {
                                "name": "material",
                                "id": "material",
                                "presentation": "markdown",
                            },
                            {
                                "name": "orientation",
                                "id": "orientation",
                                "presentation": "markdown",
                            },
                            {
                                "name": "doping",
                                "id": "doping",
                                "presentation": "markdown",
                            },
                            {
                                "name": "growth",
                                "id": "growth",
                                "presentation": "markdown",
                            },
                            {
                                "name": "responsibility",
                                "id": "responsible-user",
                                "presentation": "markdown",
                            },
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
